import unittest

from common.vars import (BROKEN_JIM, NO_ACTION, NO_TIME, NOT_BYTES,
                              NOT_DICT)
from server import parse_received_bytes


class TestparseReceivedBytesFunction(unittest.TestCase):
    def test_parse_received_bytes_not_bytes(self):
        res = parse_received_bytes('test')
        self.assertEqual(res, NOT_BYTES)

    def test_parse_received_bytes_not_json(self):
        res = parse_received_bytes(b'test')
        self.assertEqual(res, BROKEN_JIM)

    def test_parse_received_bytes_not_dict(self):
        res = parse_received_bytes(b'[111]')
        self.assertEqual(res, NOT_DICT)

    def test_parse_received_bytes_no_action(self):
        res = parse_received_bytes(b'{"time":222}')
        self.assertEqual(res, NO_ACTION)

    def test_parse_received_bytes_no_time(self):
        res = parse_received_bytes(b'{"action":111}')
        self.assertEqual(res, NO_TIME)

    def test_parse_received_bytes_ok(self):
        res = parse_received_bytes(b'{"action":111,"time":222}')
        self.assertEqual(res, {'action': 111, 'time': 222})


if __name__ == '__main__':
    unittest.main()
