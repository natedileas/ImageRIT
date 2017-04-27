import socket
import threading
import queue
import copy
import json

import effects

MSG_LEN = 4
CODE = 1111

def send(sock, obj):
    msg = json.dumps(obj)
    msglen = str(len(msg)).zfill(MSG_LEN)
    sock.send((msglen+msg).encode())

def receive(sock):
    msglen = sock.recv(MSG_LEN)

    if len(msglen) == 0:
        raise RuntimeError('msglen 0')

    msglen = int.from_bytes(msglen, "big")

    data = sock.recv(msglen).decode()

    if len(data) == 0:
        raise RuntimeError('no data recv\'d')

    print (data)
    stuff = json.loads(data)

    return stuff

class ServerThread(threading.Thread):
    def __init__(self, sock, parent, index):
        super(ServerThread, self).__init__()
        self.sock = sock
        self.serve = threading.Event()
        self.parent = parent
        self.tname = index

    def join(self, timeout=None):
        self.sock.send(b'')
        self.serve.set()
        super(ServerThread, self).join(timeout)

    def run(self):
        self.parent.status.emit('Connected: {0}'.format(self.tname))
        try:
            servercode = receive(self.sock)
            if servercode['server'] != CODE:
                raise RuntimeError('authentication failed')

            while not self.serve.isSet():
            
                data = receive(self.sock)
                
                response = ''
                if data == 'keepalive':
                    response = 'keepalive'
                elif 'bye' in data:
                    send(self.sock, 'die')
                    self.sock.close()
                    break
                elif 'selfie' in data:
                    self.parent.selfie.emit(data)
                elif 'email' in data:
                    self.parent.email.emit(data)
                else:
                    self.parent.set_state(data)

                if response:
                    send(self.sock, response)

        except RuntimeError:
            pass
        finally:
            self.parent.status.emit('Disconnected: {0}'.format(self.tname))
            self.sock.close()



from PyQt5 import QtCore

class Server(threading.Thread, QtCore.QObject):
    status = QtCore.pyqtSignal(str)
    selfie = QtCore.pyqtSignal(dict)
    email = QtCore.pyqtSignal(dict)

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self.hostname = hostname
        self.port = port
        self.serve = threading.Event()
        self.queue = queue.Queue()
        self.lock = threading.Lock()

        self._state = {}
        self.index = 0

    def join(self, timeout=None):
        self.serve.set()
        super(Server, self).join(timeout)

    def run(self):
        #self.status.emit('Disconnected')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.hostname, self.port))
        serversocket.listen(2)   # 2 connection at a time
        serversocket.settimeout(1)   # so self.serve.isSet can actually work

        while not self.serve.isSet():

            try:
                (clientsocket, address) = serversocket.accept()
                clientsocket.setblocking(1)
                self.index += 1
                st = ServerThread(clientsocket, self, self.index)
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
