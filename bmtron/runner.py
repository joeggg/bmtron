import time
import tkinter

import zmq

from .consts import UPDATE_DELAY_MS
from .display import Display
from .snake import Snake


class Runner:
    def __init__(self, num_players: int = 1) -> None:
        self.running = True
        self.started = False
        self.num_players = num_players

        self.window = tkinter.Tk()
        self.window.title("bmtron")
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.window.protocol("WM_DELETE_WINDOW", self.shut_down)

        self.display = Display(self.window)
        self.snakes: list[Snake] = [Snake(i) for i in range(num_players)]
        self.crashed_ids: list[int] = []

        ctx = zmq.Context()
        self.sck = ctx.socket(zmq.REQ)
        self.sck.connect("tcp://5.64.46.17:2302")

    def main(self) -> None:
        self.reset_game()
        while self.running:
            self.window.update()
            if self.started:
                self.window.after(UPDATE_DELAY_MS, self.update_snakes())  # type: ignore

                if len(self.crashed_ids) == self.num_players - 1:
                    time_taken = time.time() - self.begin_time
                    winner = self.find_winner()
                    self.started = False
                    self.display.display_gameover(winner, time_taken)

    def reset_game(self) -> None:
        self.crashed_ids = []
        self.display.clear()
        self.display.initialize_board()

        for snake in self.snakes:
            snake.reset_postition()
            self.display.display_snake(snake, draw_all=True)

        self.window.update()
        self.begin_time = time.time()

    def shut_down(self) -> None:
        self.running = False

    def find_winner(self) -> Snake:
        for snake in self.snakes:
            if snake.player_number not in self.crashed_ids:
                return snake

        raise Exception("No winner found")

    def mouse_input(self, _: tkinter.Event) -> None:
        self.reset_game()

    def key_input(self, event: tkinter.Event) -> None:
        for snake in self.snakes:
            if not snake.crashed:
                key_pressed = event.keysym
                # Check if the pressed key is a valid key
                if snake.is_key_valid(key_pressed):
                    self.sck.send_string(key_pressed)
                    msg = self.sck.recv()
                    print(msg)
                    self.started = True
                    snake.set_heading(key_pressed)

    def update_snakes(self) -> None:
        for snake in self.snakes:
            if snake.crashed:
                continue

            snake.update_coords()
            snake.check_if_crashed(self.snakes)

            if snake.crashed:
                self.crashed_ids.append(snake.player_number)
            else:
                self.display.display_snake(snake)
