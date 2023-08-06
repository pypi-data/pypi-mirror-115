import threading
import numpy as np
from multiprocessing import Process, shared_memory


class Service:

    def __init__(self,
                 svc_name: str,
                 svc_tag: str,
                 options: dict = {},
                 memory: list or str = None,
                 *args,
                 **kwargs):

        self.svc_name = svc_name
        self.svc_tag = svc_tag

        self.options = options
        self.memory = memory
        self.mem = {}
        self._mem = {}
        self.mem_info = {}

        if type(self.memory) == str:
            self.memory = [self.memory]

        self.args = args
        self.kwargs = kwargs

        self._alive_time = 0
        self._running = False
        self._p = self._make_process()

        self.full_stop_flag = False

        self.set_options(self.options)

    def reset(self):
        self.stop()
        self._alive_time = 0
        self._p = self._make_process()

    def set_options(self, options: dict):
        self.options = options

        self.auto_start_frame = None
        self.auto_restart_frame = None
        self.auto_stop_frame = None

        if 'auto_start' in options:
            self.auto_start_frame = options['auto_start']

        if 'auto_restart' in options and options['auto_restart']:
            self.auto_restart_frame = 2

        if 'auto_stop' in options:
            self.auto_stop_frame = options['auto_stop']

        self._handle_auto_options()

    def set_memory(self, mem_name: str, mem_info: dict):
        self.mem_info[mem_name] = mem_info
        self._mem[mem_name] = shared_memory.SharedMemory(name=mem_info['name'])
        self.mem[mem_name] = np.ndarray(shape=mem_info['shape'],
                                        dtype=mem_info['dtype'],
                                        buffer=self._mem[mem_name].buf)
        print(f'Setting {mem_name} in {self.svc_name}')

    def _make_process(self) -> Process:
        return Process(target=self.main,
                       args=self.args,
                       kwargs=self.kwargs)

    def get_svc_info(self) -> (str, str):
        return self.svc_name, self.svc_tag

    def get_params(self) -> (tuple, dict):
        return self.args, self.kwargs

    def main(self, *args, **kwargs):
        """
        Service 인스턴스를 .start()하면 main 함수를 실행한다.
        """
        raise NotImplementedError

    def start(self):
        if self._running and not self.is_alive():
            self.stop()
        if not self._running:
            self._p = self._make_process()
            self._p.start()
        self._running = True
        print(f'[{self.svc_name}] Process started.')

    def stop(self):
        if self._running:
            self._p.terminate()
        self._running = False
        print(f'[{self.svc_name}] Process stopped.')

    def full_stop(self):
        # full_stop_flag를 활용하지 않으면, _handle_auto_options가 종료되지 않는다.
        self.full_stop_flag = True
        self.set_options(options={})
        self.stop()

    def is_alive(self) -> bool:
        return self._p.is_alive()

    def _handle_auto_options(self):
        self._alive_time += 1

        if not self.full_stop_flag:

            if self.auto_start_frame is not None and self._alive_time % self.auto_start_frame == 0:
                self._auto_start()

            if self.auto_restart_frame is not None and self._alive_time % self.auto_restart_frame == 0:
                self._auto_restart()

            if self.auto_stop_frame is not None and self._alive_time % self.auto_stop_frame == 0:
                self._auto_stop()

            timer = threading.Timer(1, self._handle_auto_options)
            timer.setDaemon(True)
            timer.start()

    def _auto_start(self):
        self.start()

    def _auto_restart(self):
        if self._running and not self.is_alive():
            print(f'[{self.svc_name}] Process died. Restarting...')
            self.start()

    def _auto_stop(self):
        self.stop()


class TestService(Service):

    def main(self, param1: int, param2: int):
        import time

        cnt = 0

        while True:
            print('wow~')
            cnt += 1

            if cnt == 5:
                raise Exception('stop!')

            time.sleep(1)


class TestMemService(Service):

    def main(self):
        import time

        while True:
            print(self.mem)
            time.sleep(1)


if __name__ == '__main__':
    import time

    svc = TestService('svc-1',
                      'binance_market_stream_1',
                      options={'auto_restart': True},
                      param1=1,
                      param2=2)
    svc.start()

    while True:
        time.sleep(1)