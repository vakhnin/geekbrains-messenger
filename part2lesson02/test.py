from socket import socket, SOCK_STREAM

from common.vars import MAX_CONNECTIONS


class ServerSocketDesc:
    def __init__(self, addr='', port=7777):
        if type(port) != int or port < 0:
            raise TypeError(f'Неверный номер порта: {port}. '
                            f'Номер порта должен быть целым числом, большим нуля.')
        self._sock = socket(type=SOCK_STREAM)
        self._sock.bind((addr, port))
        self._sock.listen(MAX_CONNECTIONS)
        self._sock.settimeout(0.2)

    def __get__(self):
        return self._sock


class ServerSocket:
    def __init__(self, addr='', port=7777):
        self.sock = ServerSocketDesc(addr, port)


server_sock = ServerSocket()

conn, addr = server_sock.sock.accept()
