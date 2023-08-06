from src.base import ReqSocket


class MemoryController(ReqSocket):

    def __init__(self, host: str, port: int):
        """
        :param port: node rep_port
        """
        super().__init__(port=port, to_host=host)

    def memory_info(self, mem_name: str) -> dict:
        self._send_request('memory_info', mem_name=mem_name)
        return self._recv()

    def create_memory(self, mem_name: str, index_table: dict):
        self._send_request('create_memory',
                           mem_name=mem_name,
                           index_table=index_table)
        return self._recv()

    def delete_memory(self, mem_name: str):
        self._send_request('delete_memory', mem_name=mem_name)
        return self._recv()

    def get_data(self, filter: dict, sort_by: str = None):
        self._send_request('get_data',
                           filter=filter,
                           sort_by=sort_by)
        return self._recv()


if __name__ == '__main__':
    controller = MemoryController('localhost', 1999)