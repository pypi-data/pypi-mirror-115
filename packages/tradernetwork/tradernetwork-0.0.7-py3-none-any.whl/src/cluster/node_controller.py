from src.base import ReqSocket


class NodeController(ReqSocket):
    """
    NodeRepServer과 소통하는 ReqSocket
    """

    def __init__(self, host: str, port: int):
        """
        :param port: node rep_port
        """
        super().__init__(port=port, to_host=host)

    def get_services(self) -> list:
        self._send_request('get_services')
        return self._recv()['data'].split(';')

    def start_service(self, svc_name: str) -> dict:
        self._send_request('start_service', svc_name=svc_name)
        return self._recv()

    def stop_service(self, svc_name: str) -> dict:
        self._send_request('stop_service', svc_name=svc_name)
        return self._recv()


if __name__ == '__main__':
    controller = NodeController('localhost', 1999)
    services = controller.get_services()
    print(services)