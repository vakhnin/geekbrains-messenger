from socket import socket, SOCK_DGRAM

from common.metaclasses import ClientVerifier
from common.utils import PortDesc

# Проверка обработки ошибки при инициализации сокета для работы по UDP а не TCP
try:
    class Client(metaclass=ClientVerifier):
        def __init__(self, arg):
            self.sock = socket(arg)
            super().__init__()
except Exception as e:
    print(f'Ошибка: {e}')

try:
    class Client(metaclass=ClientVerifier):
        def __init__(self, sock):
            self.sock = sock
            super().__init__()

        def accept(self):
            return self.sock.accept()
except Exception as e:
    print(f'Ошибка: {e}')

try:
    class Client(metaclass=ClientVerifier):
        def __init__(self, sock):
            self.sock = sock
            super().__init__()

        def listen(self):
            return self.sock.listen()
except Exception as e:
    print(f'Ошибка: {e}')
