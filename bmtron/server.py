import zmq


def main():
    ctx = zmq.Context()
    rep = ctx.socket(zmq.REP)
    # 5.64.46.17
    rep.bind("tcp://127.0.0.1:2302")
    rep.setsockopt(zmq.RCVTIMEO, 1000)

    while True:
        try:
            msg = rep.recv()
            print(msg)
            rep.send(b"hello")
        except zmq.Again:
            ...


main()
