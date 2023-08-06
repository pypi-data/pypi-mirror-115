import random
from typing import Any

from src.base import RepSocket
from src.cluster.node_tracker import NodeTracker
from src.cluster.node_controller import NodeController
from src.cluster.memory_controller import MemoryController


class NoPortAvailableException(Exception):
    pass


class Cluster(RepSocket):
    """
    메인 클러스터로써 다수의 Node를 등록시키는 역할을 수행한다.
    클라이언트는 개별 Node와 소통하는 경우는 없을 것이며, 오직 클러스터를 통해서 서비스를 실행시킬 수 있다.

    * 용어:
    - 서비스: 노드에서 실행되는 서비스 프로세스 (모든 서비스는 ZeroMQ 소켓 서비스를 상속받는다)

    * 작동원리:
    1. Node가 init_node를 요청하면, rep_port, pub_port를 랜덤으로 배정해준다.
    """

    port = 6776

    def __init__(self, port_range: range):
        super().__init__(self.port)
        self.port_range = list(port_range)
        self.ports_used = []

        # Cluster의 주역할은 다수의 Node를 관리하는 것이다.
        self.tracker_port = self.port - 1
        self.node_tracker = NodeTracker(self.tracker_port)

        self.nodes = {}
        self.node_controllers = {}
        self.mem_controllers = {}
        self.node_services = {}

    def start(self):
        print('Cluster starting')
        self.start_rep_server_loop()

    def _use_available_port(self):
        if len(self.port_range) == len(self.ports_used):
            raise NoPortAvailableException
        port = random.choice(list(set(self.port_range) - set(self.ports_used)))
        self.ports_used.append(port)
        return port

    def _get_controller(self, node_name: str) -> NodeController:
        return self.node_controllers.get(node_name)

    def _update_services_info(self, node_name: str):
        controller = self._get_controller(node_name)
        if controller is not None:
            services = controller.get_services()
            self.node_services[node_name] = services

    def _get_controller_by_name(self, node_name: str, svc_name: str = None) -> NodeController:
        if node_name not in self.node_services:
            self._update_services_info(node_name)

        if svc_name in self.node_services[node_name] or svc_name is None:
            return self._get_controller(node_name)

    def get_nodes(self, **kwargs) -> (bool, str, Any):
        print('----')
        print('[get_nodes] ran successful')
        return True, '', self.nodes

    def init_node(self,
                  node_name: str,
                  node_tag: str,
                  node_host: str,
                  **kwargs) -> (bool, str, Any):
        print('-----')
        if node_name not in self.nodes:
            res_msg = f'Node: {node_name} successfully initialized'
            print(res_msg)

            rep_port = self._use_available_port()
            pub_port = self._use_available_port()
            mem_port = self._use_available_port()

            self.nodes[node_name] = {
                'host': node_host,
                'tag': node_tag,
                'rep_port': rep_port,
                'pub_port': pub_port,
                'mem_port': mem_port
            }
            self.node_controllers[node_name] = NodeController(host=node_host, port=rep_port)
            self.mem_controllers[node_name] = MemoryController(host=node_host, port=mem_port)
            return True, res_msg, self.nodes[node_name]
        else:
            res_msg = f'Node: {node_name} already exists'
            print(res_msg)
            return False, res_msg, None

    def get_services(self, node_name: str, **kwargs) -> (bool, str, Any):
        print('---')
        _ = self._get_controller_by_name(node_name)
        res_msg = 'Successfully retrieved service info for all nodes'
        return True, res_msg, self.node_services

    def _controller_response(self, node_name: str, svc_name: str, res: dict) -> (bool, str, Any):
        if res['status'] == 'SUCCESS':
            status = True
            res_msg = f'Node: {node_name}, Service: {svc_name} - {res["message"]}'
        else:
            status = False
            res_msg = f'Node: {node_name}, Service: {svc_name} - {res["message"]}'
        return status, res_msg, None

    def start_service(self, node_name: str, svc_name: str, **kwargs) -> (bool, str, Any):
        print('---')
        controller = self._get_controller_by_name(node_name, svc_name)
        res = controller.start_service(svc_name)
        return self._controller_response(node_name, svc_name, res)

    def stop_service(self, node_name: str, svc_name: str, **kwargs) -> (bool, str, Any):
        print('---')
        controller = self._get_controller_by_name(node_name, svc_name)
        res = controller.stop_service(svc_name)
        return self._controller_response(node_name, svc_name, res)


if __name__ == '__main__':
    cluster = Cluster(port_range=range(2000, 2020))
    cluster.start()