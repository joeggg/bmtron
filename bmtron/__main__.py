from __future__ import annotations
import sys

from .runner import Runner
from .server import ClientServer, HostServer


def client_main() -> None:
    host = input("Please enter a host IP address: ")
    server = ClientServer((host, 2302))
    server.connect_to_host()

    print("Waiting for host to start game...")
    num_players, player_number = server.wait_for_game_start()

    game = Runner(int(num_players), int(player_number), host=False, server=server)
    game.main()


def host_main() -> None:
    server = HostServer()
    print("Waiting for players to join...")
    server.wait_for_players()

    print("Starting game...")
    server.start_game()

    game = Runner(len(server.addresses) + 1, 0, host=True, server=server)
    game.main()


def main() -> None:
    print("****BMTron****")

    if len(sys.argv) > 1 and sys.argv[1] == "host":
        host_main()
    else:
        client_main()


if __name__ == "__main__":
    main()
