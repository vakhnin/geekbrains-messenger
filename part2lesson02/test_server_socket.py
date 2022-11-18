from socket import socket, SOCK_DGRAM, SOCK_STREAM, AF_INET

from common.metaclasses import ServerVerifier
from common.utils import PortDesc

# Проверка обработки ошибки при инициализации сокета для работы по UDP а не TCP
try:
    class ServerSocket(metaclass=ServerVerifier):
        _port = PortDesc()

        def __init__(self, addr='', port=7777):
            self._addr = addr
            self._port = port
            self._sock = None

        def start_socket(self):
            self._sock = socket(type=SOCK_DGRAM)
except Exception as e:
    print(f'Ошибка: {e}')

# Проверка обработки ошибки при использовании connect для серверного сокета
try:
    class ServerSocket(metaclass=ServerVerifier):
        _port = PortDesc()

        def __init__(self, addr='127.0.0.1', port=7777):
            self._addr = addr
            self._port = port
            self._sock = None

        def start_socket(self):
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.connect((self._addr, self._port))


    sock = ServerSocket()
    sock.start_socket()
except Exception as e:
    print(f'Ошибка: {e}')
