from __future__ import annotations
import time
import tkinter

from .consts import UPDATE_DELAY_MS
from .display import Display
from .snake import Snake
from .socket import ClientServer, HostServer


class Runner:
    def __init__(
        self,
        num_players: int,
        player_number: int,
        server: HostServer | ClientServer,
        host: bool = False,
    ) -> None:
        self.running = True
        self.started = False
        self.num_players = num_players
        self.player_number = player_number
        self.host = host

        self.window = tkinter.Tk()
        self.window.title("bmtron")
        self.window.bind("<Key>", self.key_input)
        # self.window.bind("<Button-1>", self.mouse_input)
        self.window.protocol("WM_DELETE_WINDOW", self.shut_down)

        self.display = Display(self.window)
        self.snakes: list[Snake] = [Snake(i) for i in range(num_players)]
        self.crashed_ids: set[int] = set()

        self.server = server
        self.server.set_snakes(self.snakes)

    @property
    def my_snake(self) -> Snake:
        return self.snakes[self.player_number]

    def main(self) -> None:
        self.server.start()
        self.reset_game()

        while self.running:
            self.window.update()
            if self.started:
                if type(self.server) is HostServer:
                    self.server.send_state()

                self.window.after(UPDATE_DELAY_MS, self.update_snakes())  # type: ignore

                if len(self.crashed_ids) == self.num_players - 1:
                    time_taken = time.time() - self.begin_time
                    winner = self.find_winner()
                    self.started = False
                    self.display.display_gameover(winner, time_taken)

            elif type(self.server) is ClientServer:
                self.server.wait_for_round_start()
                self.started = True

        self.server.shutdown()
        self.server.join()

    def reset_game(self) -> None:
        self.crashed_ids = set()
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
        if not self.my_snake.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.my_snake.is_key_valid(key_pressed):
                if not self.host:
                    self.server.send(f"{self.player_number},{key_pressed}".encode())
                else:
                    if not self.started:
                        self.server.send(b"started")
                        self.started = True
                    self.my_snake.set_heading(key_pressed)

    def update_snakes(self) -> None:
        with self.server.lock:
            for snake in self.snakes:
                if snake.crashed:
                    self.crashed_ids.add(snake.player_number)
                    continue

                if self.host:
                    snake.update_coords()
                    snake.check_if_crashed(self.snakes)

                self.display.display_snake(snake)
