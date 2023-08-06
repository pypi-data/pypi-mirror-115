from src.base import PullSocket, ReqSocket


class NodeTracker:

    def __init__(self, port: int):
        self.pull_socket = PullSocket(port)
        # self.req_socket = ReqSocket()


if __name__ == '__main__':
    socket = ReqSocket(8888, 'localhost')

    socket._send({'data': 1})

    try:
        res = socket._timeout_recv(3)
        print(res)
    except:
        print('timed out')