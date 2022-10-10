import json
import sys
from socket import socket, SOCK_STREAM

from common.utils import create_parser, parse_received_bytes, choice_jim_action
from common.vars import MAX_PACKAGE_LENGTH, ENCODING, MAX_CONNECTIONS

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

sock = socket(type=SOCK_STREAM)
sock.bind((namespace.a, namespace.p))
sock.listen(MAX_CONNECTIONS)

while True:
    conn, addr = sock.accept()
    print(f'Соединение установлено: {addr}')

    try:
        while True:
            try:
                data = conn.recv(MAX_PACKAGE_LENGTH)
                if not data:
                    break
                jim_obj = parse_received_bytes(data)
                answer = choice_jim_action(jim_obj)
                answer = json.dumps(answer, separators=(',', ':'))
                conn.send(answer.encode(ENCODING))
            except ConnectionResetError:
                err_msg = 'Удаленный хост принудительно разорвал ' + \
                          'существующее подключение'
                conn.close()
    finally:
        conn.close()
