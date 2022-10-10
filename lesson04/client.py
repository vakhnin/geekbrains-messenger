import sys
from socket import socket, SOCK_STREAM

from common.utils import presence_send
from common.vars import DEFAULT_IP_ADDRESS, DEFAULT_PORT

try:
    addr, port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    print('Соединение с сервером установлено')

    sock = socket(type=SOCK_STREAM)
    sock.connect((addr, port))

    presence_send(sock, 'C0deMaver1ck', 'Yep, I am here!')
except ConnectionRefusedError:
    err_msg = 'Подключение не установлено, т.к. конечный компьютер ' + \
              'отверг запрос на подключение'
    print(err_msg)
finally:
    sock.close()
    print('Соединение с сервером закрыто')
