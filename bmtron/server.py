import json
import socket
import threading
import time

from .snake import Snake


class Server(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sck.settimeout(1)
        self.running = False
        self.lock = threading.Lock()
        self.snakes: list[Snake] = []
        self.sent_packets = 0
        self.received_packets = 0

    def run(self) -> None:
        self.running = True
        while self.running:
            try:
                msg = self.sck.recv(1024)
                self.received_packets += 1
                self.handle_message(msg)
            except (TimeoutError, socket.error):
                ...

            time.sleep(0.01)

    def handle_message(self, msg: bytes) -> None:
        raise NotImplementedError

    def send(self, msg: bytes) -> None:
        self.sent_packets += 1

    def set_snakes(self, snakes: list[Snake]) -> None:
        self.snakes = snakes

    def shutdown(self) -> None:
        self.running = False


class HostServer(Server):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sck.bind(("", 2302))
        self.addresses: list[tuple[str, int]] = []

    def handle_message(self, msg: bytes) -> None:
        player_number, key = msg.decode().split(",")
        with self.lock:
            self.snakes[int(player_number)].set_heading(key)

    def send(self, msg: bytes) -> None:
        super().send(msg)
        for addr in self.addresses:
            self.sck.sendto(msg, addr)

    def send_state(self) -> None:
        data = {}
        with self.lock:
            for snake in self.snakes:
                data[snake.player_number] = {
                    "coords": [[coord.x, coord.y] for coord in snake.coords],
                    "crashed": snake.crashed,
                    "heading": snake.heading.value,
                }
        self.send(json.dumps(data).encode())

    def wait_for_players(self) -> None:
        try:
            while True:
                try:
                    msg, addr = self.sck.recvfrom(1024)
                    if msg == b"hello host":
                        self.sck.sendto(b"hello client", addr)
                        self.addresses.append(addr)
                        print(f"Player {len(self.addresses) + 1} connected")
                except (TimeoutError, socket.error):
                    ...
        except KeyboardInterrupt:
            ...

    def start_game(self) -> None:
        for i, addr in enumerate(self.addresses):
            self.sck.sendto(f"{len(self.addresses) + 1},{i+1}".encode(), addr)


class ClientServer(Server):
    def __init__(self, address: tuple[str, int], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.address = address
        self.started = False
        self.game_over = False
        self.winner = 0

    def handle_message(self, msg: bytes) -> None:
        if msg == b"started":
            self.started = True
        elif msg == b"gamestarted":
            self.game_over = False
        elif msg.startswith(b"gameover"):
            self.game_over = True
            self.winner = int(msg.split(b"#")[-1].decode())
        else:
            data = json.loads(msg.decode())
            with self.lock:
                for player, state in data.items():
                    self.snakes[int(player)].set_from_msg(state)

    def send(self, msg: bytes) -> None:
        super().send(msg)
        self.sck.sendto(msg, self.address)

    def connect_to_host(self) -> None:
        self.sck.sendto(b"hello host", self.address)
        msg = self.sck.recv(1024)
        if msg != b"hello client":
            raise Exception("Host returned invalid confirmation")

    def wait_for_game_start(self) -> tuple[int, int]:
        while True:
            try:
                msg = self.sck.recv(1024)
                num_players, player_number = msg.decode().split(",")
                return int(num_players), int(player_number)
            except (TimeoutError, socket.error):
                ...

            time.sleep(0.01)

    def wait_for_round_start(self) -> None:
        while not self.started:
            time.sleep(0.1)
        self.started = False

    def wait_for_new_round(self) -> None:
        while self.game_over:
            time.sleep(0.1)
        self.game_over = True
