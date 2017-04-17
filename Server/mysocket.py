import socket
import json

class mysocket(object):
    def __init__(self, sock=None):
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            

    def connect(self, hostname, port):
        self.sock.connect((hostname, port))

    def my_send(self, msg):
        totalsent = 0
        MSGLEN = 5

        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def my_receive(self):
        chunks = []
        bytes_recd = 0
        msg_type = self.sock.recv(1)
        if msg_type == 'm':
            MSGLEN = 5

        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

    def close(self):
        self.sock.close()

class SuperSock(socket.socket):
    MSG_LEN = 4

    def __init__(self, sock=None):
        if sock:
            self = sock.__self__
        else:
            super(SuperSock, self).__init__(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self, ip_addr, port):
        super(SuperSock, self).connect((ip_addr, port))

def send(sock, obj):
    msg = json.dumps(obj)
    msglen = str(len(msg)).zfill(SuperSock.MSG_LEN)
    sock.send((msglen+msg).encode())

def receive(sock):
    msglen = sock.recv(SuperSock.MSG_LEN)#.decode()

    if len(msglen) == 0:
        raise RuntimeError('msglen 0')

    msglen = int.from_bytes(msglen, "big") #int(msglen)
    print(msglen)

    data = sock.recv(msglen).decode()
    print(data)

    if len(data) == 0:
        raise RuntimeError('no data recv\'d')

    stuff = json.loads(data)

    return stuff