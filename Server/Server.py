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

    print (data)
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
        try:
            while not self.serve.isSet():
            
                data = receive(self.sock)
                
                response = ''
                if data == 'keepalive':
                    response = 'keepalive'
                elif 'bye' in data:
                    send(self.sock, 'die')
                    self.sock.close()
                    break
                elif 'selfie' in data:  # expect dict here containing the stuff

                    print(data)
                    timestamp = data['selfie'].get('time', None)
                    email = data['selfie'].get('email', None)

                    if timestamp:
                        self.parent.selfie_time.emit(timestamp)
                    if email:
                        self.parent.selfie_email.emit(email)
                else:
                    self.parent.set_state(data)

                if response:
                    send(self.sock, response)

        except RuntimeError:
            pass
        finally:
            self.sock.close()
            self.parent.status.emit('Disconnected')


from PyQt5 import QtCore

class Server(threading.Thread, QtCore.QObject):
    status = QtCore.pyqtSignal(str)
    selfie_time = QtCore.pyqtSignal(str)
    selfie_email = QtCore.pyqtSignal(str)

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self.hostname = hostname
        self.port = port
        self.serve = threading.Event()
        self.queue = queue.Queue()
        self.lock = threading.Lock()

        self._state = {}

    def join(self, timeout=None):
        self.serve.set()
        super(Server, self).join(timeout)

    def run(self):
        # temporary disabling; is probaling causing a recursive repair issue, threading related
        self.status.emit('Disconnected')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.hostname, self.port))
        serversocket.listen(2)   # 2 connection at a time
        serversocket.settimeout(1)   # so self.serve.isSet can actually work

        while not self.serve.isSet():

            try:
                (clientsocket, address) = serversocket.accept()
                self.status.emit('Connected')
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
