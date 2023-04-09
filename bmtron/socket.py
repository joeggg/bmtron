import json
import socket
import threading

from .snake import Snake


class Server(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sck.settimeout(1)
        self.running = True
        self.lock = threading.Lock()
        self.snakes: list[Snake] = []

    def run(self) -> None:
        while self.running:
            try:
                self.listen()
            except TimeoutError:
                ...

    def listen(self) -> None:
        raise NotImplementedError

    def send(self, msg: bytes) -> None:
        raise NotImplementedError

    def set_snakes(self, snakes: list[Snake]) -> None:
        self.snakes = snakes

    def shutdown(self) -> None:
        self.running = False


class HostServer(Server):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sck.bind(("", 2302))
        self.addresses: list[tuple[str, int]] = []

    def listen(self) -> None:
        msg = self.sck.recv(1024)
        player_number, key = msg.decode().split(",")
        with self.lock:
            self.snakes[int(player_number)].set_heading(key)

    def send(self, msg: bytes) -> None:
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
                except TimeoutError:
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

    def listen(self) -> None:
        msg = self.sck.recv(1024)
        data = json.loads(msg.decode())
        with self.lock:
            for player, state in data.items():
                self.snakes[int(player)].set_from_msg(state)

    def send(self, msg: bytes) -> None:
        self.sck.sendto(msg, self.address)

    def connect_to_host(self) -> None:
        self.sck.sendto(b"hello host", self.address)
        msg = self.sck.recv(1024)
        if msg != b"hello client":
            raise Exception("Host returned invalid confirmation")

    def wait_for_game_start(self) -> tuple[int, int]:
        while self.running:
            try:
                msg = self.sck.recv(1024)
                num_players, player_number = msg.decode().split(",")
                return int(num_players), int(player_number)
            except TimeoutError:
                ...

        raise Exception("Exited server before receiving game info")

    def wait_for_round_start(self) -> None:
        while self.running:
            try:
                msg = self.sck.recv(1024)
                if msg == b"started":
                    return
            except TimeoutError:
                ...

        raise Exception("Exited server before starting round")
