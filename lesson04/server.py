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
from socket import socket, SOCK_STREAM

from common.utils import create_parser, make_answer, parse_presence

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

sock = socket(type=SOCK_STREAM)
sock.bind((namespace.a, namespace.p))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    print(f'Соединение установлено: {addr}')

    try:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                jim_obj = json.loads(data.decode('utf-8'))
                if 'action' not in jim_obj.keys():
                    answer = make_answer(400,
                                         {'error': 'Request has no "action"'})
                elif 'time' not in jim_obj.keys():
                    answer = make_answer(400,
                                         {'error': 'Request has no "time""'})
                else:
                    if jim_obj['action'] == 'presence':
                        answer = parse_presence(jim_obj)
                    else:
                        answer = make_answer(400,
                                             {'error': 'Unknown action'})
                answer = json.dumps(answer, separators=(',', ':'))
                conn.send(answer.encode('utf-8'))
            except json.JSONDecodeError:
                answer = make_answer(400, {'error': 'JSON broken'})
                answer = json.dumps(answer, separators=(',', ':'))
                conn.send(answer.encode('utf-8'))
            except ConnectionResetError:
                err_msg = 'Удаленный хост принудительно разорвал ' + \
                          'существующее подключение'
                conn.close()
    finally:
        conn.close()
