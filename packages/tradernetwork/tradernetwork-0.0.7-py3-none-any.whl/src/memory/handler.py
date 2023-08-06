from typing import Any, Dict
from functools import reduce

from src.base import RepSocket
from src.memory.memory import Memory
from src.memory.index import IndexHandler


class MemoryHandler(RepSocket):

    def __init__(self, port: int):
        super().__init__(port)

        self.memory_table: Dict[str, Memory] = {}
        self.memory_index: Dict[str, dict] = {}
        self.full_index_table = None

    def _get_memory_info(self, mem_name: str) -> dict:
        mem = self.memory_table.get(mem_name)
        if isinstance(mem, Memory):
            return mem.mem_info

    def _get_memory_index(self, mem_name: str) -> dict:
        mem = self.memory_table.get(mem_name)
        if isinstance(mem, Memory):
            return mem.index_table

    def memory_info(self, mem_name: str, **kwargs) -> (bool, str, Any):
        mem_info = self._get_memory_info(mem_name)
        if mem_info is not None:
            res_msg = 'Successfully retrieved memory info'
            return True, res_msg, mem_info
        else:
            res_msg = 'No such memory exists'
            return False, res_msg, None

    def create_memory(self, mem_name: str, index_table: dict, **kwargs) -> (bool, str, Any):
        try:
            res_msg = 'Successfully created memory'
            self.memory_table[mem_name] = Memory(mem_name, index_table)
            self.memory_index[mem_name] = self._get_memory_index(mem_name)
            self.full_index_table = IndexHandler.merge_index(self.memory_index)
            mem_info = self._get_memory_info(mem_name)
            return True, res_msg, mem_info
        except Exception as e:
            res_msg = str(e)
            return False, res_msg, None

    def delete_memory(self, mem_name: str, **kwargs) -> (bool, str, Any):
        try:
            res_msg = 'Successfully deleted memory'
            del self.memory_table[mem_name]
            del self.memory_index[mem_name]
            self.full_index_table = IndexHandler.merge_index(self.memory_index)
            return True, res_msg, None
        except Exception as e:
            res_msg = str(e)
            return False, res_msg, None

    def get_data(self, filter: dict, sort_by: str = None, **kwargs) -> (bool, str, Any):
        try:
            reqs = IndexHandler.make_memory_request(self.full_index_table, filter)

            data = []

            for mem_name, req in reqs.items():
                mem = self.memory_table[mem_name]
                d = mem.get(req)
                data.append(d)

            data = reduce(lambda x, y: x + y, data, [])

            if sort_by is not None:
                data = sorted(data, key=lambda k: k[sort_by])

            res_msg = 'Successfully retrieved data'

            return True, res_msg, data
        except Exception as e:
            res_msg = str(e)
            return False, res_msg, None


if __name__ == '__main__':
    index = {
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

    index_1, index_2 = IndexHandler.split_index(index, 'second', 2)

    mh = MemoryHandler(999)
    mh.create_memory('mem-1', index_1)
    mh.create_memory('mem-2', index_2)

    filter = {'second': {'from': '090000', 'to': '090003'},
              'symbol': ['BTC']}

    data = mh.get_data(filter)

    print(mh)