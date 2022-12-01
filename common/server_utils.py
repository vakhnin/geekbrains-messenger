import argparse
import json
import logging
import sys
from socket import socket, SOCK_STREAM

from storage.server_storage import Storage
from .metaclasses import ServerVerifier
from .utils import Log
from .vars import DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, NOT_BYTES, \
    NOT_DICT, NO_ACTION, NO_TIME, BROKEN_JIM, UNKNOWN_ACTION, MAX_CONNECTIONS, LOGIN_ERROR, LOGIN_OK

import logs.client_log_config
import logs.server_log_config

client_log = logging.getLogger('messenger.client')
server_log = logging.getLogger('messenger.server')


class PortDesc:
    def __init__(self):
        super().__init__()
        self._port = None

    def __set__(self, instance, port):
        if type(port) != int or port < 0:
            raise ValueError(f'Неверный номер порта: {port}. '
                             f'Номер порта должен быть целым числом, большим или равным нулю.')
        self._port = port

    def __get__(self, instance, instance_type):
        return self._port


class Server(metaclass=ServerVerifier):
    _port = PortDesc()

    def __init__(self, engine, addr='', port=7777):
        self._addr = addr
        self._port = port
        self._sock = None
        self.storage = Storage(engine)

    def start_socket(self):
        self._sock = socket(type=SOCK_STREAM)
        self._sock.bind((self._addr, self._port))
        self._sock.listen(MAX_CONNECTIONS)
        self._sock.settimeout(0.5)

    def accept(self):
        return self._sock.accept()

    def read_requests(self, r_clients, clients_data):
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
                    if jim_obj['action'] == 'login':
                        if 'user' in jim_obj.keys() \
                                and 'password' in jim_obj.keys():
                            if self.login(jim_obj['user'], jim_obj['password']):
                                answer = make_answer(LOGIN_OK)
                                answer = json.dumps(answer, separators=(',', ':'))
                                clients_data[sock]['client_name'] = jim_obj['user']
                                self.storage.user_add(jim_obj['user'])
                                self.storage.history_time_add(
                                    clients_data[sock]['client_name'],
                                    clients_data[sock]['client_addr'][0]
                                )
                                clients_data[sock]['answ_for_send'].append(answer)
                                continue
                        answer = make_answer(LOGIN_ERROR)
                        answer = json.dumps(answer, separators=(',', ':'))
                        clients_data[sock]['answ_for_send'].append(answer)
                    elif jim_obj['action'] == 'presence':
                        if 'user' in jim_obj.keys() \
                                and isinstance(jim_obj['user'], dict) \
                                and 'client_name' in jim_obj['user'].keys():
                            # clients_data[sock]['client_name'] = \
                            #     jim_obj['user']['client_name']
                            # self.storage.user_add(jim_obj['user']['client_name'])
                            # self.storage.history_time_add(
                            #     clients_data[sock]['client_name'],
                            #     clients_data[sock]['client_addr'][0]
                            # )
                            continue
                    elif jim_obj['action'] == 'msg':
                        for _, value in clients_data.items():
                            if jim_obj['to'] == '#' \
                                    or jim_obj['to'] == value['client_name'] \
                                    or jim_obj['from'] == value['client_name']:
                                value['msg_for_send'].append(msg)
                    elif jim_obj['action'] == 'get_contacts':
                        contact_list = self.storage.contact_list_by_login(clients_data[sock]['client_name'])
                        answer = make_answer(202, {'alert': f'{contact_list}'})
                        answer = json.dumps(answer, separators=(',', ':'))
                        clients_data[sock]['answ_for_send'].append(answer)
                    elif jim_obj['action'] == 'add_contact':
                        if self.storage.contact_add(jim_obj['user_login'], jim_obj['user_id']):
                            contact_list = self.storage.contact_list_by_login(clients_data[sock]['client_name'])
                            answer = make_answer(202, {'alert': f'{contact_list}'})
                        else:
                            answer = make_answer(500)
                        answer = json.dumps(answer, separators=(',', ':'))
                        clients_data[sock]['answ_for_send'].append(answer)
                    elif jim_obj['action'] == 'del_contact':
                        if self.storage.contact_del(jim_obj['user_login'], jim_obj['user_id']):
                            contact_list = self.storage.contact_list_by_login(clients_data[sock]['client_name'])
                            answer = make_answer(202, {'alert': f'{contact_list}'})
                        else:
                            answer = make_answer(500)
                        answer = json.dumps(answer, separators=(',', ':'))
                        clients_data[sock]['answ_for_send'].append(answer)
            except Exception:
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                sock.close()
                del clients_data[sock]

    def login(self, user, password):
        if password == '12345':
            return True
        return False


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
        except Exception as e:
            print(e)
            print(
                f'Клиент {sock.fileno()} {sock.getpeername()} отключился'
            )
            sock.close()
            del clients_data[sock]
