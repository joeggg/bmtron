from __future__ import annotations
import threading
import time
import tkinter

from .consts import UPDATE_DELAY_MS
from .display import Display
from .server import ClientServer, HostServer
from .snake import Snake


class Runner(threading.Thread):
    def __init__(
        self,
        window: tkinter.Tk,
        server: HostServer | ClientServer,
        num_players: int,
        player_number: int,
    ) -> None:
        super().__init__()
        self.running = True
        self.started = False  # Round has started
        self.game_over = False  # Waiting on the gameover screen
        self.num_players = num_players
        self.player_number = player_number
        self.host = type(server) is HostServer
        self.begin_time = 0.0

        self.window = window
        self.window.title("bmtron")
        self.window.bind("<Key>", self.key_input)

        if self.host:
            self.window.bind("<Button-1>", self.mouse_input)

        self.display = Display(self.window)
        self.snakes: list[Snake] = [Snake(i) for i in range(num_players)]
        self.crashed_ids: set[int] = set()

        self.server = server
        self.server.set_snakes(self.snakes)

        def shut_down() -> None:
            nonlocal self
            self.running = False
            self.server.shutdown()
            self.server.join()
            window.quit()

        self.window.protocol("WM_DELETE_WINDOW", shut_down)

    @property
    def my_snake(self) -> Snake:
        return self.snakes[self.player_number]

    def run(self) -> None:
        self.reset_game()

        while self.running:
            if self.started:
                if type(self.server) is HostServer:
                    self.server.send_state()

                self.window.after(UPDATE_DELAY_MS, self.update_snakes())  # type: ignore

                if type(self.server) is ClientServer:
                    if self.server.game_over:
                        self.stop_round()
                else:
                    if len(self.crashed_ids) == self.num_players - 1:
                        self.stop_round()

            elif type(self.server) is ClientServer:
                if self.game_over:
                    self.server.wait_for_new_round()
                    self.reset_game()
                else:
                    self.server.wait_for_round_start()
                    self.start_round()

    def reset_game(self) -> None:
        self.crashed_ids = set()
        self.display.clear()
        self.display.initialize_board()

        for snake in self.snakes:
            snake.reset_postition()
            self.display.display_snake(snake, draw_all=True)

        self.window.update()
        self.game_over = False

        if type(self.server) is ClientServer:
            self.server.game_over = False
        else:
            self.server.send(b"gamestarted")

    def start_round(self) -> None:
        self.started = True
        self.begin_time = time.time()

    def stop_round(self) -> None:
        if type(self.server) is ClientServer:
            winner = self.snakes[self.server.winner]
        else:
            winner = self.find_winner()
            self.server.send(f"gameover#{winner.player_number}".encode())

        time_taken = time.time() - self.begin_time
        self.started = False
        self.game_over = True
        self.display.display_gameover(winner, time_taken)
        print(
            f"Packets sent: {self.server.sent_packets}, packets received: {self.server.received_packets}"
        )

    def shut_down(self) -> None:
        self.running = False

    def find_winner(self) -> Snake:
        for snake in self.snakes:
            if snake.player_number not in self.crashed_ids:
                return snake

        raise Exception("No winner found")

    def mouse_input(self, _: tkinter.Event) -> None:
        if self.game_over:
            self.reset_game()

    def key_input(self, event: tkinter.Event) -> None:
        if not self.game_over and not self.my_snake.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.my_snake.is_key_valid(key_pressed):
                if not self.host:
                    self.server.send(f"{self.player_number},{key_pressed}".encode())
                else:
                    if not self.started:
                        self.server.send(b"started")
                        self.start_round()
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

                if not snake.crashed:
                    self.display.display_snake(snake)
