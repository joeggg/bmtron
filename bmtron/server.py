import socket


def main():
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(("", 2302))
    sck.settimeout(1)

    print("Starting server")
    while True:
        try:
            msg, addr = sck.recvfrom(1024)
            print(msg)
            sck.sendto(b"confirmed", addr)
        except TimeoutError:
            ...
        except KeyboardInterrupt:
            break

    print("Shut down")


main()
