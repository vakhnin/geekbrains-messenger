# Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
#
# * клиент отправляет запрос серверу;
# * сервер отвечает соответствующим кодом результата.
#
# Клиент и сервер должны быть реализованы в виде отдельных скриптов,
# содержащих соответствующие функции.
# Функции клиента:
# * сформировать presence-сообщение;
# * отправить сообщение серверу;
# * получить ответ сервера; разобрать сообщение сервера;
# * параметры командной строки скрипта client.py <addr> [<port>]:
#   addr — ip-адрес сервера;
#   port — tcp-порт на сервере, по умолчанию 7777.
# Функции сервера:
# * принимает сообщение клиента;
# * формирует ответ клиенту;
# * отправляет ответ клиенту;
# * имеет параметры командной строки:
#   -p <port> — TCP-порт для работы (по умолчанию использует 7777);
#   -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
import json
import sys
from datetime import datetime
from socket import socket, SOCK_STREAM


def presence_send(sock_, account_name, status):
    jim_msg = {
        'action': 'presence',
        'time': datetime.now().timestamp(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status,
        }
    }
    msg = json.dumps(jim_msg, separators=(',', ':'))
    sock_.send(msg.encode('utf-8'))
    try:
        data = sock.recv(1024)
        jim_obj = json.loads(data.decode('utf-8'))
        print(jim_obj)
    except json.JSONDecodeError:
        print('Answer JSON broken')


try:
    addr, port = 'localhost', 7777
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
