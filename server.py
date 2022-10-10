import json
import sys
from socket import socket, SOCK_STREAM

from common.utils import create_parser, make_answer, parse_presence
from common.vars import MAX_PACKAGE_LENGTH, ENCODING

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
                data = conn.recv(MAX_PACKAGE_LENGTH)
                if not data:
                    break
                jim_obj = json.loads(data.decode(ENCODING))
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
                conn.send(answer.encode(ENCODING))
            except ConnectionResetError:
                err_msg = 'Удаленный хост принудительно разорвал ' + \
                          'существующее подключение'
                conn.close()
    finally:
        conn.close()
