import threading
from typing import Any

from src.base import *
from src.memory import MemoryHandler
from src.service.service_table import ServiceTable


class NodePortException(Exception):
    pass


class Node(ReqSocket):

    def __init__(self,
                 node_name: str,
                 node_tag: str,
                 port: int,
                 node_host: str = 'localhost',
                 to_host: str = 'localhost',
                 service_table: ServiceTable = {}):

        super().__init__(port, to_host)

        self.node_name = node_name
        self.node_tag = node_tag
        self.node_host = node_host

        self.service_table = service_table
        self.running_services = {}

    def run_node_rep_server(self, port: int):
        self.rep_server = NodeRepServer(self, port)
        print(f'[{self.node_name}] Started Rep Server at: {port}\n')
        self.rep_server.start_rep_server_loop()

    def run_node_pub_server(self, port: int):
        self.pub_server = PubSocket(port)
        print(f'[{self.node_name}] Started Pub Server at: {port}\n')

    def run_mem_rep_server(self, port: int):
        self.mem_server = MemoryHandler(port)
        print(f'[{self.node_name}] Started Mem Server at: {port}\n')
        self.mem_server.start_rep_server_loop()

    def restart_node(self):
        """
        TODO
        """
        pass

    def start_service(self, svc_name: str, **kwargs) -> (bool, str, Any):
        if svc_name in self.service_table:
            if svc_name not in self.running_services:
                res_msg = f'Service: {svc_name} successfully started'
                service = self.service_table[svc_name]['service']
                params = self.service_table[svc_name]['params']

                svc = service(**params)

                # locking onto pre-existing shared memory class if it is already defined on the Node
                if svc.memory is not None:
                    for mem_name in svc.memory:
                        if mem_name in self.mem_server.memory_table:
                            svc.set_memory(mem_name, self.mem_server.memory_info(mem_name)[-1])

                self.running_services[svc_name] = svc
                self.running_services[svc_name].start()
            else:
                res_msg = f'Service: {svc_name} is already running'
            return True, res_msg, None
        else:
            res_msg = f'Service: {svc_name} does not exist'
            return False, res_msg, None

    def stop_service(self, svc_name: str, **kwargs) -> (bool, str, Any):
        if svc_name in self.service_table:
            if svc_name in self.running_services:
                res_msg = f'Service: {svc_name} successfully stopped'
                self.running_services[svc_name].full_stop()
                del self.running_services[svc_name]
            else:
                res_msg = f'Service: {svc_name} is not running'
            return True, res_msg, None
        else:
            res_msg = f'Service: {svc_name} does not exist'
            return False, res_msg, None

    def memory_info(self, mem_name: str, **kwargs) -> (bool, str, Any):
        return self.mem_server.memory_info(mem_name)

    def create_memory(self, mem_name: str, index_table: dict, **kwargs) -> (bool, str, Any):
        return self.mem_server.create_memory(mem_name, index_table)

    def delete_memory(self, mem_name: str) -> (bool, str, Any):
        return self.mem_server.delete_memory(mem_name)

    def get_data(self, filter: dict, sort_by: str = None, **kwargs) -> (bool, str, Any):
        return self.mem_server.get_data(filter, sort_by)

    def start(self,
              rep_port: int = None,
              pub_port: int = None,
              mem_port: int = None):

        self._send_request('init_node',
                           node_name=self.node_name,
                           node_tag=self.node_tag,
                           node_host=self.node_host)

        try:
            """
            Cluster가 올라가 있다면 cluster로부터 rep_port, pub_port를 받아서 소켓 서버들을 실행한다.
            """
            res = self._timeout_recv(5)

            if res.get('status') == 'SUCCESS':
                print(f'- Node: {self.node_name}, Role: {self.node_tag} connected\n')

                data = res.get('data')

                rep_port = data.get('rep_port')
                pub_port = data.get('pub_port')
                mem_port = data.get('mem_port')

        except OSError:
            print('Failed to connect to Cluster server. Starting standalone server.')

            if rep_port is None or pub_port is None or mem_port is None:
                raise NodePortException

        t1 = threading.Thread(target=self.run_node_rep_server, args=(rep_port,))
        t1.start()

        t2 = threading.Thread(target=self.run_mem_rep_server, args=(mem_port,))
        t2.start()

        self.run_node_pub_server(pub_port)


class NodeRepServer(RepSocket):

    def __init__(self, node: Node, port: int):
        super().__init__(port)

        self.node = node

    def get_services(self) -> (bool, str, Any):
        res_msg = f'Successfully retrieved {self.node.node_name} services'
        return True, res_msg, self.node.service_table.get_services()

    def start_service(self, svc_name: str, **kwargs) -> (bool, str, Any):
        return self.node.start_service(svc_name)

    def stop_service(self, svc_name: str, **kwargs) -> (bool, str, Any):
        return self.node.stop_service(svc_name)


if __name__ == '__main__':
    from src.memory import IndexHandler
    from src.service.service import TestService, TestMemService

    services = {
        'svc-1': {
            'service': TestMemService,
            'params': {
                'svc_name': 'svc-1',
                'svc_tag': 'binance_market_stream_1',
                'memory': ['mem-1', 'mem-2'],
            }
        },
        'svc-2': {
            'service': TestService,
            'params': {
                'svc_name': 'svc-2',
                'svc_tag': 'binance_market_stream_2',
                'options': {'auto_start': 10, 'auto_stop': 20},
                'param1': 2,
                'param2': 3
            }
        }
    }

    mem_index = {
        'second': {
            '090000': 0,
            '090001': 1,
            '090002': 2,
            '090003': 3,
            '090004': 4,
            '090005': 5,
            '090006': 6
        },
        'symbol': {
            'BTC': 0,
            'ETH': 1,
            'XRP': 2
        },
        'field': {
            'open': 0,
            'high': 1,
            'low': 2,
            'close': 3,
            'volume': 4
        }
    }

    svc_table = ServiceTable(services)
    node = Node('node-1', 'binance_market_1', 6776, service_table=svc_table)
    node.start(rep_port=1999, pub_port=1998, mem_port=1997)

    index_1, index_2 = IndexHandler.split_index(mem_index, 'second', 2)
    node.create_memory('mem-1', index_1)
    node.create_memory('mem-2', index_2)

    node.start_service('svc-1')
