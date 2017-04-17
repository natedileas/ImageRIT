import socket
import threading
import queue
from mysocket import SuperSock, send, receive

class ServerThread(threading.Thread):
    def __init__(self, sock, queue):
        super(ServerThread, self).__init__()
        self.sock = sock
        self.serve = threading.Event()
        self.queue = queue

    def join(self, timeout=None):
        self.serve.set()
        super(DisplayServer, self).join(timeout)

    def run(self):
        while not self.serve.isSet():
            try:
                data = receive(self.sock)
                print(data)
                #self.queue.put(data)

                if data == 'keepalive':
                    response = 'keepalive'
                if data == 'bye':
                    send(self.sock, 'die')
                    self.sock.close()
                    break
                if data == 'set me up scotty':
                    with open('untitled.ui','r') as f:
                        response = f.read()

                send(self.sock, response)

            except RuntimeError:
                self.sock.close()
                print('RuntimeError, socket closed')
                break

class Server(threading.Thread):
    def __init__(self, hostname, port):
        super(Server, self).__init__()
        self.hostname = hostname
        self.port = port
        self.serve = threading.Event()
        self.queue = queue.Queue()

    def join(self, timeout=None):
        self.serve.set()
        super(Server, self).join(timeout)

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.hostname, self.port))
        serversocket.listen(2)   # 2 connection at a time
        serversocket.settimeout(1)   # so self.serve.isSet can actually work

        while not self.serve.isSet():

            try:
                (clientsocket, address) = serversocket.accept()
                clientsocket.setblocking(1)
                st = ServerThread(clientsocket, self.queue)
                st.start()
            except socket.timeout:
                continue

    def get_state(self):
        return {}
        l = threading.Lock()
        l.aquire()
        s = s.state
        l.release()
        return s

    def set_state(self):
        # take a dictionary
        # update values of keys
        # be able to clear a key-value pair
        # modify a global-state dictionary based on a configuration
        pass

    
if __name__ == '__main__':

    hostname = 'localhost'
    port = 49912

    server = Server(hostname, port)
    server.run()
