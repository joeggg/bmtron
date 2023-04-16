from __future__ import annotations
import sys
import tkinter

from .runner import Runner
from .server import ClientServer, HostServer


def main() -> None:
    print("****BMTron****")
    window = tkinter.Tk()
    server: ClientServer | HostServer

    if len(sys.argv) > 1 and sys.argv[1] == "host":
        input("hi")
        server = HostServer(window)
        print("Waiting for players to join...")
        # server.addresses = [("localhost", 1), ("localhost", 1), ("localhost", 1)]
        num_players, player_number = server.wait_for_players()

        print("Starting game...")
        server.start_game()

    else:
        host = input("Please enter a host IP address: ")
        server = ClientServer(window, (host, 2302))
        server.connect_to_host()

        print("Waiting for host to start game...")
        num_players, player_number = server.wait_for_game_start()

    game = Runner(window, server, num_players, player_number)
    game.start()

    try:
        window.mainloop()
    except KeyboardInterrupt:
        game.shut_down()
        game.join()
        window.quit()


if __name__ == "__main__":
    main()
