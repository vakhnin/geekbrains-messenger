import argparse
import functools
import json
import logging
import re
import sys
import time
import traceback
from socket import socket, SOCK_STREAM

from .vars import DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, NOT_BYTES, \
    NOT_DICT, NO_ACTION, NO_TIME, BROKEN_JIM, UNKNOWN_ACTION, MAX_CONNECTIONS

import logs.client_log_config
import logs.server_log_config

client_log = logging.getLogger('messenger.client')
server_log = logging.getLogger('messenger.server')


class Log:
    """Класс-декоратор"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        if sys.argv[0].endswith('server.py'):
            logger = server_log
        else:
            logger = client_log
        res = self.func(*args, **kwargs)
        logger.debug((f'Функция {self.func.__name__}() '
                      f'вызвана из функции {traceback.extract_stack()[-2].name}()'))
        logger.debug(f'Функция: {self.func.__name__}({args}, {kwargs}) = {res}')
        return res


# Функции и классы сервера
class PortDesc:
    def __init__(self):
        super().__init__()
        self._port = None

    def __set__(self, instance, port):
        if type(port) != int or port < 0:
            raise TypeError(f'Неверный номер порта: {port}. '
                            f'Номер порта должен быть целым числом, большим нуля.')
        self._port = port

    def __get__(self, instance, instance_type):
        return self._port


class ServerSocket:
    _port = PortDesc()

    def __init__(self, addr='', port=7777):
        self._addr = addr
        self._port = port
        self._sock = None

    def start_socket(self):
        self._sock = socket(type=SOCK_STREAM)
        self._sock.bind((self._addr, self._port))
        self._sock.listen(MAX_CONNECTIONS)
        self._sock.settimeout(0.5)

    def accept(self):
        return self._sock.accept()


def get_server_param():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='')
    parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    namespace = parser.parse_args(sys.argv[1:])
    return {
        'addr': namespace.a,
        'port': namespace.p
    }


@Log
def parse_received_bytes(data):
    if not isinstance(data, bytes):
        return NOT_BYTES
    try:
        jim_obj = json.loads(data.decode(ENCODING))
        if not isinstance(jim_obj, dict):
            return NOT_DICT
        elif 'action' not in jim_obj.keys():
            return NO_ACTION
        elif 'time' not in jim_obj.keys():
            return NO_TIME
        return jim_obj
    except json.JSONDecodeError:
        server_log.error(BROKEN_JIM)
        return BROKEN_JIM


@Log
def choice_jim_action(jim_obj):
    if jim_obj == NOT_BYTES:
        return make_answer(500, {})
    elif jim_obj in (NO_ACTION, NO_TIME, BROKEN_JIM):
        return make_answer(400, {'error': jim_obj})
    else:
        if jim_obj['action'] == 'presence':
            return parse_presence(jim_obj)
        else:
            return make_answer(400, {'error': UNKNOWN_ACTION})


@Log
def make_answer(code, message={}):
    answer = {'response': code}
    if 'error' in message.keys():
        answer['error'] = message['error']
    elif 'alert' in message.keys():
        answer['alert'] = message['alert']
    return answer


@Log
def parse_presence(jim_obj):
    if 'user' not in jim_obj.keys():
        return make_answer(400, {'error': 'Request has no "user"'})
    elif type(jim_obj['user']) != dict:
        return make_answer(400, {'error': '"user" is not dict'})
    elif 'account_name' not in jim_obj['user'].keys():
        return make_answer(400, {'error': '"user" has no "account_name"'})
    elif not jim_obj['user']['account_name']:
        return make_answer(400, {'error': '"account_name" is empty'})
    else:
        print(f'User {jim_obj["user"]["account_name"]} is presence')
        if 'status' in jim_obj['user'].keys() \
                and jim_obj['user']['status']:
            print(f'Status user{jim_obj["user"]["account_name"]} is "' +
                  jim_obj['user']['status'] + '"')
        return make_answer(200)


@Log
def read_requests(r_clients, clients_data):
    for sock in r_clients:
        if sock not in clients_data.keys():
            return
        try:
            msg = sock.recv(MAX_PACKAGE_LENGTH).decode('utf-8')
            try:
                jim_obj = json.loads(msg)
            except json.JSONDecodeError:
                server_log.error(f'Brocken jim {msg}')
                continue

            answer = make_answer(200)
            answer = json.dumps(answer, separators=(',', ':'))
            clients_data[sock]['answ_for_send'].append(answer)

            if not isinstance(jim_obj, dict):
                server_log.error(f'Data not dict {jim_obj}')
                continue
            if 'action' in jim_obj.keys():
                if jim_obj['action'] == 'presence':
                    if 'user' in jim_obj.keys() \
                            and isinstance(jim_obj['user'], dict) \
                            and 'client_name' in jim_obj['user'].keys():
                        clients_data[sock]['client_name'] = \
                            jim_obj['user']['client_name']
                        continue
                elif jim_obj['action'] == 'msg':
                    for _, value in clients_data.items():
                        if jim_obj['to'] == '#' \
                                or jim_obj['to'] == value['client_name']:
                            value['msg_for_send'].append(msg)
        except Exception:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            del clients_data[sock]


@Log
def write_responses(w_clients, clients_data):
    for sock in w_clients:
        if sock not in clients_data.keys():
            return
        try:
            if len(clients_data[sock]['answ_for_send']):
                msg = clients_data[sock]['answ_for_send'].pop()
                sock.send(msg.encode('utf-8'))
            elif len(clients_data[sock]['msg_for_send']):
                msg = clients_data[sock]['msg_for_send'].pop()
                sock.send(msg.encode('utf-8'))
        except Exception:
            print(
                f'Клиент {sock.fileno()} {sock.getpeername()} отключился'
            )
            sock.close()
            del clients_data[sock]


# Функции клиента
@Log
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='localhost')
    parser.add_argument('-n', default='Guest')
    parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    namespace = parser.parse_args(sys.argv[1:])

    return namespace.a, namespace.p, namespace.n


@Log
def parse_answer(jim_obj):
    if not isinstance(jim_obj, dict):
        print('Server answer not dict')
        return
    if 'response' in jim_obj.keys():
        print(f'Server answer: {jim_obj["response"]}')
    else:
        print('Answer has not "response" code')
    if 'error' in jim_obj.keys():
        print(f'Server error message: {jim_obj["error"]}')
    if 'alert' in jim_obj.keys():
        print(f'Server alert message: {jim_obj["alert"]}')


@Log
def make_presence_message(client_name, status):
    return {
        'action': 'presence',
        'time': time.time(),
        'type': 'status',
        'user': {
            'client_name': client_name,
            'status': status,
        }
    }


@Log
def make_msg_message(client_name, msg, to='#'):
    return {
        'action': 'msg',
        'time': time.time(),
        'to': to,
        'from': client_name,
        'encoding': 'utf-8',
        'message': msg,
    }


@Log
def send_message_take_answer(sock, msg):
    msg = json.dumps(msg, separators=(',', ':'))
    try:
        sock.send(msg.encode(ENCODING))
        data = sock.recv(MAX_PACKAGE_LENGTH)
        return json.loads(data.decode(ENCODING))
    except json.JSONDecodeError:
        client_log.error('Answer JSON broken')
        return {}


@Log
def cmd_help():
    print('Поддерживаемые команды:')
    print('m [сообщение] - отправить сообщение в общий чат.')
    print('p [получатель] [сообщение] - отправить приватное сообщение.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@Log
def user_input(sock, client_name):
    try:
        cmd_help()
        while True:
            msg = input('Введите команду: \n')
            msg = msg.strip()
            msg = re.split('\\s+', msg)
            if msg[0] == 'exit':
                break
            elif msg[0] == 'help':
                cmd_help()
                continue
            elif msg[0] == 'm':
                if len(msg) < 2:
                    print('Неверное количество аргументов команды.'
                          'Введите "help" для вывода списка команд')
                    continue
                msg = make_msg_message(client_name, ' '.join(msg[1:]))
            elif msg[0] == 'p':
                if len(msg) < 3:
                    print('Неверное количество аргументов команды.'
                          'Введите "help" для вывода списка команд')
                    continue
                msg = make_msg_message(client_name, ' '.join(msg[2:]), msg[1])
            else:
                print('Команда не распознана. '
                      'Введите "help" для вывода списка команд')
                continue

            msg = json.dumps(msg, separators=(',', ':'))
            sock.send(msg.encode(ENCODING))
    except Exception as e:
        client_log.debug(f'Ошибка выходного потока {e}')


@Log
def user_output(sock, client_name):
    try:
        while True:
            data = sock.recv(MAX_PACKAGE_LENGTH)
            if not data:
                break
            try:
                jim_obj = json.loads(data.decode(ENCODING))
            except json.JSONDecodeError:
                client_log.error(f'Brocken jim {data}')
                continue
            if not isinstance(jim_obj, dict):
                client_log.error(f'Data not dict {jim_obj}')
                continue
            if 'response' in jim_obj.keys():
                client_log.debug(f'Получен ответ сервера {jim_obj["response"]}')
                continue
            if 'action' in jim_obj.keys():
                if jim_obj['action'] == 'msg':
                    if 'from' in jim_obj.keys() \
                            and 'message' in jim_obj.keys():
                        if 'to' in jim_obj.keys() \
                                and jim_obj['to'] == '#':
                            print(
                                f'{jim_obj["from"]}> {jim_obj["message"]}'
                            )
                        else:
                            print(
                                f'{jim_obj["from"]} (private)> '
                                f'{jim_obj["message"]}'
                            )
    except Exception as e:
        client_log.debug(f'Ошибка входного потока{e}')
