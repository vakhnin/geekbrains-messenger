import argparse
from datetime import datetime
import json

from vars import DEFAULT_PORT


# Функции сервера
def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-a', default='')
    parser_.add_argument('-p', type=int, default=DEFAULT_PORT)
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


# Функции клиента
def presence_send(sock_, account_name, status):
    jim_msg = {
        'action': 'presence',
        'time': datetime.now().timestamp(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status,
        }
    }
    msg = json.dumps(jim_msg, separators=(',', ':'))
    sock_.send(msg.encode('utf-8'))
    try:
        data = sock_.recv(1024)
        jim_obj = json.loads(data.decode('utf-8'))
        parse_answer(jim_obj)
    except json.JSONDecodeError:
        print('Answer JSON broken')


def parse_answer(jim_obj):
    if 'response' in jim_obj.keys():
        print(f'Server response: {jim_obj["response"]}')
    else:
        print('Answer has not "response" code')
    if 'error' in jim_obj.keys():
        print(f'Server error message: {jim_obj["error"]}')
    if 'alert' in jim_obj.keys():
        print(f'Server alert message: {jim_obj["alert"]}')
