import itertools
import numpy as np
from typing import Any, Dict, List
from collections import OrderedDict
from multiprocessing import shared_memory


class Memory:

    def __init__(self,
                 mem_name: str,
                 index_table: Dict[str, Dict[str, int]]):
        """
        index_table = {
            'second': {'0900': 0, '0901': 1, ... },
            'exchange': {'kiwoom': 0, 'ebest': 1, ... },
            'field': {'open': 0, 'high': 1, ... }
        }
        """

        self.mem_name = mem_name
        self.index_table = index_table

        self.mem_shape = tuple(len(index) for _, index in self.index_table.items())

        np_array = np.zeros(self.mem_shape)
        np_array.fill(np.nan)

        self.mem_dtype = np_array.dtype
        self.mem_size = np_array.nbytes

        self.mem = shared_memory.SharedMemory(create=True, size=self.mem_size)
        self.mem_array = np.ndarray(shape=self.mem_shape,
                                    dtype=self.mem_dtype,
                                    buffer=self.mem.buf)
        self.mem_array[:] = np_array[:]
        del np_array

        print('Shared Memory array를 생성하였습니다.')
        print(
            f'[Second Bar Array] Memory: {self.mem.name} / Shape: {self.mem_shape} / Size: {self.mem_size / 1e6} MBs\n'
        )

        self.mem_info = {
            'name': self.mem.name,
            'shape': self.mem_shape,
            'dtype': str(self.mem_dtype),
            'size': self.mem_size,
            **{f'{key}_table': val for key, val in index_table.items()}
        }

    def get(self, index_filter: Dict[str, List[int]]) -> List[Dict[str, Any]]:
        ordered_filter = OrderedDict()

        for key, _ in self.index_table.items():
            if key in index_filter:
                ordered_filter[key] = index_filter[key]

        index_filter_keys = list(ordered_filter.keys())
        index_filter_values = list(ordered_filter.values())

        last_idx = index_filter_values[-1]

        idx_opts = index_filter_values[:-1]
        idx_comb = list(itertools.product(*idx_opts))
        idx_comb = [tuple([*comb, last_idx]) for comb in idx_comb]

        data = []

        for comb in idx_comb:
            d = {}

            if len(comb) >= 2:
                for i, idx in enumerate(comb[:-1]):
                    key = index_filter_keys[i]
                    index_table = {v: k for k, v in self.index_table[key].items()}
                    idx_name = index_table[idx]
                    d[key] = idx_name

            index_table = {v: k for k, v in self.index_table[index_filter_keys[-1]].items()}
            idx_names = [index_table[c] for c in comb[-1]]

            mem_data = self.mem_array[comb]
            d = {**d, **dict(zip(idx_names, mem_data))}

            data.append(d)

        return data


if __name__ == '__main__':
    import pandas as pd

    mem = Memory('mem-1', {
        'index_1': {'a': 0, 'b': 1, 'c': 2},
        'index_2': {'a': 0, 'b': 1},
        # 'index_3': {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
    })

    print(mem.mem_info)

    mem.mem_array[0, 0] = 1
    mem.mem_array[0, 1] = 1

    mem.mem_array[1, 0] = 2
    mem.mem_array[1, 1] = 2

    mem.mem_array[2, 0] = 3
    mem.mem_array[2, 1] = 3

    index_filter = {'index_1': [0, 1], 'index_2': [0, 1]}
    data = mem.get(index_filter)
    print(data)