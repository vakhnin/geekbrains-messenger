import unittest

from common.utils import make_presence_message


class TestMakePresenceMessageFunction(unittest.TestCase):
    def test_parse_answer_not_dict(self):
        data = {'action': 'presence',
                'time': 1593079094.211563,
                'type': 'status',
                'user': {'account_name': 'test name',
                         'status': 'test status'}}
        res = make_presence_message('test name', 'test status')
        data['time'] = res['time']
        self.assertEqual(res, data)


if __name__ == '__main__':
    unittest.main()
