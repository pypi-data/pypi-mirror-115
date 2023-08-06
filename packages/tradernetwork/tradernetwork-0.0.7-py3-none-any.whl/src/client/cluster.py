from src.base import ReqSocket


class ClusterClient(ReqSocket):
    """
    클러스터와 소통할 수 있는 클라이언트
    """

    def __init__(self, port: int = 6776, to_host: str = 'localhost'):
        super().__init__(port, to_host)

    def get_nodes(self):
        self._send_request('get_nodes')
        return self._recv()

    def get_services(self, node_name: str):
        self._send_request('get_services', node_name=node_name)
        return self._recv()

    def start_service(self, node_name: str, svc_name: str):
        self._send_request('start_service',
                           node_name=node_name,
                           svc_name=svc_name)
        return self._recv()

    def stop_service(self, node_name: str, svc_name: str):
        self._send_request('stop_service',
                           node_name=node_name,
                           svc_name=svc_name)
        return self._recv()


if __name__ == '__main__':
    cc = ClusterClient()
    # nodes = cc.get_nodes()['data']
    services = cc.get_services('node-1')
    print(services)