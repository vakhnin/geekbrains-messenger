import argparse
import json
import logging
import re
import sys
import time

from .metaclasses import ClientVerifier
from .utils import Log
from .vars import DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING

import logs.client_log_config
import logs.server_log_config

client_log = logging.getLogger('messenger.client')
server_log = logging.getLogger('messenger.server')


class Client(metaclass=ClientVerifier):
    def __init__(self, sock):
        self.sock = sock
        super().__init__()

    def connect(self, arg):
        self.sock.connect(arg)


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


def make_get_contacts_message(client_name):
    return {
        'action': 'get_contacts',
        'time': time.time(),
        'user_login': client_name,
        'encoding': 'utf-8',
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
    print('c получить список контактов с сервера.')
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
            elif msg[0] == 'c' or msg[0] == 'с':
                msg = make_get_contacts_message(client_name)
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
                if jim_obj['response'] == 202:
                    print(f'Список контактов: {jim_obj["alert"]}')
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
