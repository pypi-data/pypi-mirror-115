from functools import reduce
from typing import Dict, List


class IndexHandler:

    @classmethod
    def split_index(cls,
                    index_table: dict,
                    split_on: str,
                    split_cnt: int) -> list:

        index_cnt = len(index_table[split_on])
        index_cutoff = index_cnt // split_cnt

        response = []

        for i in range(split_cnt):
            idx_start = i * index_cutoff
            idx_end = (i + 1) * index_cutoff if i != split_cnt - 1 else index_cnt
            new_index = list(index_table[split_on].keys())[idx_start:idx_end]
            response.append(
                {
                    **index_table,
                    split_on: {
                        idx: i for i, idx in enumerate(new_index)
                    }
                }
            )

        return response

    @classmethod
    def merge_index(cls, index_table_by_name: dict) -> dict:
        idx_t = {}
        for mem_name, index_table in index_table_by_name.items():
            idx_t[mem_name] = {
                key: {k: {mem_name: v} for k, v in val.items()}
                for key, val in index_table.items()
            }

        unique_index = list(set(reduce(lambda x, y: x + y,
                                       [list(t.keys()) for _, t in idx_t.items()],
                                       [])))

        final_idx = {}
        for index in unique_index:
            final_idx[index] = {}
            for mem_name, index_table in idx_t.items():
                for idx_key, idx_val in index_table[index].items():
                    if idx_key not in final_idx[index]:
                        final_idx[index][idx_key] = {}
                    final_idx[index][idx_key].update(idx_val)

        return final_idx

    @classmethod
    def make_memory_request(cls,
                            full_index_table: dict,
                            index_filter: dict) -> Dict[str, Dict[str, List[int]]]:
        """
        :param full_index_table: IndexHandler.merge_index 함수를 통해서 리턴받은 dictionary
        :param index_filter:

        --> {
            'second': {'from': '090000', 'to': '090010'},
            'symbol': ['BTC', 'ETH']
        }

        field 옵션은 제외하였는데, 모든 field 값을 요청한다는 뜻이다.

        :return ex) {'mem-0': {'symbol': [0], 'field': [0, 1, 2, 3, 4]},
                     'mem-1': {'symbol': [0], 'field': [0, 1, 2, 3, 4]},
                     'mem-2': {'symbol': [0], 'field': [0, 1, 2, 3, 4], 'second': [0, 1, 2]}}
        """

        filtered_index_table = {}

        for index, index_table in full_index_table.items():
            if index in index_filter:
                detail = index_filter[index]
                index_keys = list(index_table.keys())

                if type(detail) == list:
                    index_list = [key for key in detail if key in index_keys]

                elif type(detail) == dict:
                    if 'count' in detail:
                        index_cnt = int(detail['count'])
                        index_list = index_keys[-index_cnt:]
                    else:
                        index_from = detail.get('from', index_keys[0])
                        index_to = detail.get('to', index_keys[-1])
                        index_list = [key for key in index_keys if index_from <= key <= index_to]

                else:
                    raise Exception('filters should be provided as list or dict format')

                filtered_index_table = {
                    **filtered_index_table,
                    index: {key: val for key, val in index_table.items() if key in index_list}
                }

            else:
                filtered_index_table = {
                    **filtered_index_table,
                    index: index_table
                }

        reqs = {}
        for index, index_table in filtered_index_table.items():
            for field, info in index_table.items():
                for mem_name, idx in info.items():
                    if mem_name not in reqs:
                        reqs[mem_name] = {}

                    if index not in reqs[mem_name]:
                        reqs[mem_name] = {**reqs[mem_name], index: [idx]}
                    else:
                        reqs[mem_name][index].append(idx)

        return reqs


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

    idx_list = IndexHandler.split_index(index, 'second', 3)

    index_table_by_name = {
        f'mem-{i}': idx_list[i]
        for i in range(len(idx_list))
    }

    idx_table = IndexHandler.merge_index(index_table_by_name)

    reqs = IndexHandler.make_memory_request(idx_table, {
        'second': {'count': 3},
        'symbol': ['BTC']
    })
    print(reqs)