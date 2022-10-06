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
import json
import sys
from socket import socket, SOCK_STREAM


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-a', default='')
    parser_.add_argument('-p', type=int, default=7777)
    return parser_


def make_answer(code, message=None):
    answer_ = {'response': code}
    if not message:
        return answer_
    if 'error' in message.keys():
        answer_['error'] = message['error']
    elif 'alert' in message.keys():
        answer_['alert'] = message['alert']
    return answer_


def parse_presence(jim_obj_):
    if 'user' not in jim_obj_.keys():
        return make_answer(400, {'error': 'Request has no "user"'})
    elif type(jim_obj_['user']) != dict:
        return make_answer(400, {'error': '"user" is not dict'})
    elif 'account_name' not in jim_obj_['user'].keys():
        return make_answer(400, {'error': '"user" has no "account_name"'})
    elif not jim_obj_['user']['account_name']:
        return make_answer(400, {'error': '"account_name" is empty'})
    else:
        print(f'User {jim_obj_["user"]["account_name"]} is presence')
        if 'status' in jim_obj_['user'].keys() \
                and jim_obj_['user']['status']:
            print(f'Status user{jim_obj_["user"]["account_name"]} is "' +
                  jim_obj_['user']['status'] + '"')
        return make_answer(200)


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
