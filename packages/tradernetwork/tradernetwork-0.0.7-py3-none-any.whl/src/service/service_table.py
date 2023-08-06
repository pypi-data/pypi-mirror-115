from src.service.service import Service


class ServiceTable:

    def __init__(self, services: dict = {}):
        """
        :param services: {'svc-1': {'service': TestService, 'params': {'svc_name': 'svc-1', ... }}
        """
        self.table = {}
        if services != {}:
            for svc_name, svc_info in services.items():
                self.add_service(svc_name, **svc_info)

    def __contains__(self, svc_name: str):
        return svc_name in self.table

    def __getitem__(self, svc_name: str):
        return self.table.get(svc_name)

    def get_services(self) -> str:
        return ';'.join(list(self.table.keys()))

    def add_service(self, svc_name: str, service: Service, params: dict = {}):
        self.table[svc_name] = {
            'service': service,
            'params': params
        }


if __name__ == '__main__':
    from src.service.service import TestService

    services = {
        'svc-1': {
            'service': TestService,
            'params': {
                'svc_name': 'svc-1',
                'svc_tag': 'binance_market_stream_1',
                'options': {'auto_start': 5, 'auto_stop': 10},
                'param1': 1,
                'param2': 2
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

    svc_table = ServiceTable(services)

    print(svc_table.table)

    print('svc-1' in svc_table)

    print(svc_table['svc-1'])
    print(svc_table['svc-3'])