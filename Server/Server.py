import socket
import threading
import queue
import copy
import json

import effects

MSG_LEN = 4

def send(sock, obj):
    msg = json.dumps(obj)
    msglen = str(len(msg)).zfill(MSG_LEN)
    sock.send((msglen+msg).encode())

def receive(sock):
    msglen = sock.recv(MSG_LEN)#.decode()

    if len(msglen) == 0:
        raise RuntimeError('msglen 0')

    msglen = int.from_bytes(msglen, "big")

    data = sock.recv(msglen).decode()

    if len(data) == 0:
        raise RuntimeError('no data recv\'d')

    stuff = json.loads(data)

    return stuff

class ServerThread(threading.Thread):
    def __init__(self, sock, parent):
        super(ServerThread, self).__init__()
        self.sock = sock
        self.serve = threading.Event()
        self.parent = parent


    def join(self, timeout=None):
        self.serve.set()
        super(ServerThread, self).join(timeout)

    def run(self):
        while not self.serve.isSet():
            try:
                response = ''
                data = receive(self.sock)
                
                self.parent.set_state(data)

                if data == 'keepalive':
                    response = 'keepalive'
                if data == 'bye':
                    send(self.sock, 'die')
                    self.sock.close()
                    break

                send(self.sock, response)

            except RuntimeError:
                self.sock.close()
                self.parent.status.showMessage('Disconnected')
                break

class Server(threading.Thread):
    def __init__(self, hostname, port, status):
        super(Server, self).__init__()
        self.hostname = hostname
        self.port = port
        self.serve = threading.Event()
        self.queue = queue.Queue()
        self.lock = threading.Lock()

        self.status = status

        self._state = {}

    def join(self, timeout=None):
        self.serve.set()
        super(Server, self).join(timeout)

    def run(self):
        self.status.showMessage('Disconnected')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.hostname, self.port))
        serversocket.listen(2)   # 2 connection at a time
        serversocket.settimeout(1)   # so self.serve.isSet can actually work

        while not self.serve.isSet():

            try:
                (clientsocket, address) = serversocket.accept()
                self.status.showMessage('Connected')
                clientsocket.setblocking(1)
                st = ServerThread(clientsocket, self)
                st.start()
            except socket.timeout:
                continue

    def get_state(self):
        with self.lock:        
            s = copy.deepcopy(self._state)
        return s

    def set_state(self, new_dict):
        # modify a global-state dictionary
        with self.lock:
            for key, val in new_dict.items():
                print(key, val)
                if val:
                    self._state[key] = effects.config.config[key]

                    if isinstance(val, list):
                        self._state[key]['args'] = val
                else:
                    self._state.pop(key, None)

if __name__ == '__main__':

    hostname = 'localhost'
    port = 49912

    server = Server(hostname, port)
    server.run()
