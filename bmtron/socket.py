import socket


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
