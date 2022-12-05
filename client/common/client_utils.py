import argparse
import datetime
import json
import logging
import re
import sys

from PyQt5 import QtCore

sys.path.append('..')
from storage.client_storage import ClientStorage
from .metaclasses import ClientVerifier
from .utils import Log
from .vars import DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, LOGIN_OK, LOGIN_ERROR

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
        'time': str(datetime.datetime.now()),
        'type': 'status',
        'user': {
            'client_name': client_name,
            'status': status,
        }
    }


def make_login_message(client_name, password):
    return {
        'action': 'login',
        'time': str(datetime.datetime.now()),
        'user': client_name,
        'password': password,
    }


@Log
def make_msg_message(client_name, msg, to='#'):
    return {
        'action': 'msg',
        'time': str(datetime.datetime.now()),
        'to': to,
        'from': client_name,
        'encoding': 'utf-8',
        'message': msg,
    }


def make_get_contacts_message(client_name):
    return {
        'action': 'get_contacts',
        'time': str(datetime.datetime.now()),
        'user_login': client_name,
        'encoding': 'utf-8',
    }


def make_add_contact_message(client_name, contact_name):
    return {
        'action': 'add_contact',
        'user_id': contact_name,
        'time': str(datetime.datetime.now()),
        'user_login': client_name,
    }


def make_del_contact_message(client_name, contact_name):
    return {
        'action': 'del_contact',
        'user_id': contact_name,
        'time': str(datetime.datetime.now()),
        'user_login': client_name,
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
    print('a [имя пользователя] добавить пользователя в список контактов.')
    print('d [имя пользователя] удалить пользователя из списка контактов.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


def message_to_str(jim_obj, client_name):
    if 'from' in jim_obj.keys() \
            and 'message' in jim_obj.keys():
        if 'to' in jim_obj.keys() \
                and jim_obj['to'] == '#':
            return f'{jim_obj["from"]}> {jim_obj["message"]}'
        elif jim_obj['from'] == client_name:
            return f'{jim_obj["from"]}->{jim_obj["to"]} (private)> {jim_obj["message"]}'
        else:
            return f'{jim_obj["from"]} (private)> {jim_obj["message"]}'


class Sender(QtCore.QThread):
    def __init__(self, sock, client_name, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sock = sock
        self.client_name = client_name

    def run(self):
        try:
            cmd_help()
            while True:
                msg = input('Введите команду: \n')
                msg = msg.strip()
                msg = re.split('\\s+', msg)
                if msg[0] == 'exit':
                    sys.exit()
                elif msg[0] == 'help':
                    cmd_help()
                    continue
                elif msg[0] == 'c' or msg[0] == 'с':
                    msg = make_get_contacts_message(self.client_name)
                elif msg[0] == 'a' or msg[0] == 'а':
                    msg = make_add_contact_message(self.client_name, msg[1])
                elif msg[0] == 'd':
                    msg = make_del_contact_message(self.client_name, msg[1])
                elif msg[0] == 'm':
                    if len(msg) < 2:
                        print('Неверное количество аргументов команды.'
                              'Введите "help" для вывода списка команд')
                        continue
                    msg = make_msg_message(self.client_name, ' '.join(msg[1:]))
                elif msg[0] == 'p':
                    if len(msg) < 3:
                        print('Неверное количество аргументов команды.'
                              'Введите "help" для вывода списка команд')
                        continue
                    msg = make_msg_message(self.client_name, ' '.join(msg[2:]), msg[1])
                else:
                    print('Команда не распознана. '
                          'Введите "help" для вывода списка команд')
                    continue

                msg = json.dumps(msg, separators=(',', ':'))
                self.sock.send(msg.encode(ENCODING))
        except Exception as e:
            client_log.debug(f'Ошибка выходного потока {e}')


class Receiver(QtCore.QThread):
    login_server_answer_code_signal = QtCore.pyqtSignal(int)
    new_message_signal = QtCore.pyqtSignal(object)
    new_contact_list_signal = QtCore.pyqtSignal(object)

    def __init__(self, sock, client_name, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sock = sock
        self.storage = None
        self.client_name = client_name
        self.is_client_name_set = False

    def set_new_client_name(self, client_name):
        self.client_name = client_name
        self.storage = ClientStorage(self.client_name)
        self.is_client_name_set = True

    def run(self):
        try:
            while True:
                data = self.sock.recv(MAX_PACKAGE_LENGTH)
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
                        contact_list = jim_obj["alert"]
                        contact_list = contact_list.replace("'", '"')
                        contact_list = json.loads(contact_list)
                        self.new_contact_list_signal.emit(contact_list)
                        print(f'Список контактов: {jim_obj["alert"]}')
                    elif jim_obj['response'] in (LOGIN_OK, LOGIN_ERROR):
                        self.login_server_answer_code_signal.emit(jim_obj['response'])
                    continue
                if 'action' in jim_obj.keys():
                    if jim_obj['action'] == 'msg':
                        print(message_to_str(jim_obj, self.client_name))
                        if self.storage:
                            self.storage.add_message(jim_obj['from'],
                                                     jim_obj['to'], jim_obj['time'], jim_obj['message'])
                            self.new_message_signal.emit(jim_obj)
        except Exception as e:
            client_log.debug(f'Ошибка входного потока{e}')
