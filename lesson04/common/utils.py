import argparse


# Функции сервера
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
