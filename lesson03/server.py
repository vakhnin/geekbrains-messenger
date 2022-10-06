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
import argparse
import sys
from socket import socket, SOCK_STREAM


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-a', default='')
    parser_.add_argument('-p', type=int, default=7777)
    return parser_


parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

sock = socket(type=SOCK_STREAM)
sock.bind((namespace.a, namespace.p))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    print(f'Соединение установлено: {addr}')
