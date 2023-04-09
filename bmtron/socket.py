import socket
import threading


class Socket:
    def __init__(self, host: str) -> None:
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (host, 2302)

    def send(self, msg) -> None:
        self.sck.sendto(msg, self.addr)

    def recv(self) -> bytes:
        return self.sck.recv(1024)

    def set_timeout(self) -> None:
        self.sck.settimeout(1)

    def unset_timeout(self) -> None:
        self.sck.settimeout(None)


class Server(threading.Thread):
    def __init__(
        self, sck: socket.socket, addresses: list[tuple[str, int]], *args, **kwargs
    ) -> None:
        self.sck = sck
        self.addresses = addresses
        self.running = True
        super().__init__(*args, **kwargs)

    def run(self) -> None:
        while self.running:
            try:
                msg = self.sck.recv(1024)
                print(msg)
            except TimeoutError:
                ...

    def shutdown(self) -> None:
        self.running = False

    def send(self, msg: bytes) -> None:
        for addr in self.addresses:
            self.sck.sendto(msg, addr)
