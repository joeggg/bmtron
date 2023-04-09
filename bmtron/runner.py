from __future__ import annotations
import time
import tkinter


from .consts import UPDATE_DELAY_MS
from .display import Display
from .snake import Snake
from .socket import Server, Socket


class Runner:
    def __init__(
        self,
        num_players: int = 1,
        player_number: int = 0,
        server: Server | None = None,
        client_socket: Socket | None = None,
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
        self.crashed_ids: list[int] = []

        if self.host:
            self.server = server
        else:
            self.socket = client_socket

    @property
    def my_snake(self) -> Snake:
        return self.snakes[self.player_number]

    def main(self) -> None:
        if self.host:
            self.server.start()  # type: ignore

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

            elif not self.host:
                msg = self.socket.recv()  # type: ignore
                if msg == b"started":
                    print("Started")
                    self.started = True

        if self.host:
            self.server.shutdown()  # type: ignore
            self.server.join()  # type: ignore

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
        if not self.my_snake.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.my_snake.is_key_valid(key_pressed):
                if not self.host:
                    self.socket.send(key_pressed.encode())  # type: ignore
                    msg = self.socket.recv()  # type: ignore
                    self.my_snake.set_from_msg(msg)
                else:
                    if not self.started:
                        self.server.send(b"started")  # type: ignore
                        self.started = True
                    self.my_snake.set_heading(key_pressed)

    def update_snakes(self) -> None:
        for snake in self.snakes:
            if snake.crashed:
                continue

            if self.host:
                snake.update_coords()
                snake.check_if_crashed(self.snakes)

            if snake.crashed:
                self.crashed_ids.append(snake.player_number)
            else:
                self.display.display_snake(snake)
