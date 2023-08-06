import zmq
import json
from typing import Dict

from src.base import SubSocket, PullSocket


class ProxySocket:
    """
    여러 SUB 소켓을 proxy해주는 역할 수행
    """

    def __init__(self, sockets: Dict[str, SubSocket or PullSocket]):
        self.sockets = sockets
        self.socket_names = {}

        self.poller = zmq.Poller()

        for name, sock in self.sockets.items():
            self.socket_names[sock.socket] = name
            self.poller.register(sock.socket, zmq.POLLIN)

    def callback(self, socket_name: str, data: dict):
        raise NotImplementedError

    def start_proxy_server_loop(self):
        while True:
            socks = dict(self.poller.poll())

            for socket in socks:
                socket_name = self.socket_names[socket]
                data = socket.recv_string()
                data = json.loads(data)
                self.callback(socket_name, data)


if __name__ == '__main__':
    from src.base import PushSocket

    p1 = PushSocket(100)
    p1.publish({'data': 1})

    p2 = PushSocket(101)
    p2.publish({'data': 2})

    sockets = {
        'push_1': PullSocket(100),
        'push_2': PullSocket(101)
    }

    def callback(socket_name, data):
        print(socket_name, data)

    proxy = ProxySocket(sockets)
    proxy.callback = callback
    proxy.start_proxy_server_loop()