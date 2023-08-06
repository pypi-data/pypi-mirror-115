import zmq
import json
import traceback


class Socket:

    protocol = None

    def __init__(self, port: int, to_host: str = 'localhost'):
        self.ctx = zmq.Context()
        self.port = port
        self.to_host = to_host

        self.connect()

    def connect(self):
        if self.protocol == 'REP':
            self._start_rep_server()

        elif self.protocol == 'REQ':
            self._start_req_server()

        elif self.protocol == 'NO_LINGER_REQ':
            self._start_no_linger_req_server()

        elif self.protocol == 'PUB':
            self._start_pub_server()

        elif self.protocol == 'SUB':
            self._start_sub_server()

        elif self.protocol == 'PUSH':
            self._start_push_server()

        elif self.protocol == 'PULL':
            self._start_pull_server()

    def exit(self):
        self.socket.close()
        self.ctx.term()

    def reconnect(self):
        self.exit()
        self.connect()

    def _recv(self):
        return json.loads(self.socket.recv_string())

    def _timeout_recv(self, timeout_secs: int):
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        if poller.poll(timeout_secs * 1000):
            return self.socket.recv_json()
        else:
            raise IOError('Socket receive timed out')

    def _send(self, message: dict):
        self.socket.send_string(json.dumps(message))

    def publish(self, message: dict):
        self._send(message)

    def _send_response(self, status: str, message: str, data: dict = {}):
        response = {'status': status, 'message': message, 'data': data}
        self.socket.send_string(json.dumps(response))

    def _send_request(self, method, **params):
        request = {'method': method, 'params': params}
        self.socket.send_string(json.dumps(request))

    def _start_rep_server(self):
        self.socket = self.ctx.socket(zmq.REP)
        self.socket.bind(f'tcp://*:{self.port}')

    def _start_req_server(self):
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.connect(f'tcp://{self.to_host}:{self.port}')

    def _start_no_linger_req_server(self):
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.connect(f'tcp://{self.to_host}:{self.port}')

    def _start_pub_server(self):
        self.socket = self.ctx.socket(zmq.PUB)
        self.socket.bind(f'tcp://*:{self.port}')

    def _start_sub_server(self):
        self.socket = self.ctx.socket(zmq.SUB)
        self.socket.connect(f'tcp://{self.to_host}:{self.port}')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def _start_push_server(self):
        self.socket = self.ctx.socket(zmq.PUSH)
        self.socket.connect(f'tcp://{self.to_host}:{self.port}')

    def _start_pull_server(self):
        self.socket = self.ctx.socket(zmq.PULL)
        self.socket.bind(f'tcp://*:{self.port}')

    def start_rep_server_loop(self):
        while True:
            req = self._recv()
            method = req.get('method')
            params = req.get('params')
            try:
                if method is None:
                    self._send_response('FAILED', 'method is required')
                else:
                    f = getattr(self, method)
                    status, message, data = f(**params)
                    if status == 0 or not status:
                        self._send_response('FAILED',
                                            message if message is not None else '',
                                            data if data is not None else {})
                    else:
                        self._send_response('SUCCESS',
                                            message if message is not None else '',
                                            data if data is not None else {})
            except AttributeError:
                traceback.print_exc()
                self._send_response('FAILED', 'no such method')
            except TypeError:
                traceback.print_exc()
                self._send_response('FAILED', 'wrong parameters')


class RepSocket(Socket):
    protocol = 'REP'

class ReqSocket(Socket):
    protocol = 'REQ'

class NoLingerReqSocket(Socket):
    protocol = 'NO_LINGER_REQ'

class PubSocket(Socket):
    protocol = 'PUB'

class SubSocket(Socket):
    protocol = 'SUB'

class PushSocket(Socket):
    protocol = 'PUSH'

class PullSocket(Socket):
    protocol = 'PULL'