import argparse
import json
import sys
import logging
from datetime import datetime
from socket import socket, SOCK_STREAM

from .vars import DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, NOT_BYTES, \
    NOT_DICT, NO_ACTION, NO_TIME, BROKEN_JIM, UNKNOWN_ACTION, MAX_CONNECTIONS, DEFAULT_IP_ADDRESS

import logs.client_log_config
import logs.server_log_config

client_log = logging.getLogger('messenger.client')
server_log = logging.getLogger('messenger.server')


# Функции сервера
def make_listen_socket():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='')
    parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    namespace = parser.parse_args(sys.argv[1:])

    sock = socket(type=SOCK_STREAM)
    sock.bind((namespace.a, namespace.p))
    sock.listen(MAX_CONNECTIONS)
    return sock


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
        server_log.debug(f'User {jim_obj_["user"]["account_name"]} is presence')
        if 'status' in jim_obj_['user'].keys() \
                and jim_obj_['user']['status']:
            server_log.debug(f'Status user{jim_obj_["user"]["account_name"]} is "' +
                  jim_obj_['user']['status'] + '"')
        return make_answer(200)


# Функции клиента
def make_sent_socket():
    addr, port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    sock = socket(type=SOCK_STREAM)
    sock.connect((addr, port))

    return sock


def make_presence_message(account_name, status):
    return {
        'action': 'presence',
        'time': datetime.now().timestamp(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status,
        }
    }


def send_message_take_answer(sock, msg):
    msg = json.dumps(msg, separators=(',', ':'))
    try:
        sock.send(msg.encode(ENCODING))
        data = sock.recv(MAX_PACKAGE_LENGTH)
        return json.loads(data.decode(ENCODING))
    except json.JSONDecodeError:
        client_log.error('Answer JSON broken')
        return {}


def parse_answer(jim_obj):
    if not isinstance(jim_obj, dict):
        client_log.error('Server answer not dict')
        return
    if 'response' in jim_obj.keys():
        client_log.debug(f'Server answer: {jim_obj["response"]}')
    else:
        client_log.error('Answer has not "response" code')
    if 'error' in jim_obj.keys():
        client_log.error(f'Server error message: {jim_obj["error"]}')
    if 'alert' in jim_obj.keys():
        client_log.error(f'Server alert message: {jim_obj["alert"]}')
