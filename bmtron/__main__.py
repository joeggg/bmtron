from __future__ import annotations
import socket
import sys
from .runner import Runner
from .socket import Socket


def host_main() -> None:
    print("****BMTron****")
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.settimeout(1)
    addresses: list[tuple[str, int]] = []

    while True:
        try:
            msg, addr = sck.recvfrom(1024)
            if msg == b"hello host":
                sck.sendto(b"hello client", addr)
                addresses.append(addr)
                print(f"Player {len(addresses) + 1} connected")
        except TimeoutError:
            ...
        except KeyboardInterrupt:
            break

    print("Starting game...")


def main() -> None:
    print("****BMTron****")
    host = input("Please enter a host IP address: ")
    sck = Socket(host)

    sck.send(b"hello host")
    msg = sck.recv()
    if msg != b"hello client":
        print(msg)
        print("Somethings wrong")
        return

    print("Waiting for host to start game...")
    msg = sck.recv()  # e.g. 2,1
    num_players, player_number = msg.decode().split(",")

    game = Runner(sck, int(num_players), int(player_number), False)
    game.main()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "host":
        host_main()
    else:
        main()
