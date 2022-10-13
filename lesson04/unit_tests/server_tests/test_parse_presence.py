import unittest

from common.utils import parse_presence


class TestParsePresenceFunction(unittest.TestCase):
    def test_parse_presence_no_user(self):
        jim_obj = {'action': 'presence', 'time': 1593004547.839623,
                   'type': 'status',
                   'user-NO': {
                       'account_name': 'C0deMaver1ck',
                       'status': 'Yep, I am here!'}
                   }
        res = parse_presence(jim_obj)
        self.assertEqual(res, {'response': 400,
                               'error': 'Request has no "user"'})

    def test_parse_presence_user_not_dict(self):
        jim_obj = {'action': 'presence', 'time': 1593004547.839623,
                   'type': 'status',
                   'user': 'C0deMaver1ck'
                   }
        res = parse_presence(jim_obj)
        self.assertEqual(res, {'response': 400,
                               'error': '"user" is not dict'})

    def test_parse_presence_user_no_account_name(self):
        jim_obj = {'action': 'presence', 'time': 1593004547.839623,
                   'type': 'status',
                   'user': {
                       'account_name-NO': 'C0deMaver1ck',
                       'status': 'Yep, I am here!'}
                   }
        res = parse_presence(jim_obj)
        self.assertEqual(res, {'response': 400,
                               'error': '"user" has no "account_name"'})

    def test_parse_presence_user_account_name_is_empty(self):
        jim_obj = {'action': 'presence', 'time': 1593004547.839623,
                   'type': 'status',
                   'user': {
                       'account_name': '',
                       'status': 'Yep, I am here!'}
                   }
        res = parse_presence(jim_obj)
        self.assertEqual(res, {'response': 400,
                               'error': '"account_name" is empty'})

    def test_parse_presence_user_account_ok(self):
        jim_obj = {'action': 'presence', 'time': 1593004547.839623,
                   'type': 'status',
                   'user': {
                       'account_name': 'C0deMaver1ck',
                       'status': 'Yep, I am here!'}
                   }
        res = parse_presence(jim_obj)
        self.assertEqual(res, {'response': 200})


if __name__ == '__main__':
    unittest.main()
