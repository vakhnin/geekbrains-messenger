import unittest

from common.utils import make_answer


class TestMakeAnswerFunction(unittest.TestCase):
    def test_make_answer_code_only(self):
        res = make_answer(200)
        self.assertEqual(res, {'response': 200})

    def test_make_answer_alert(self):
        res = make_answer(200, {'alert': 'code and alert'})
        self.assertEqual(res, {'response': 200, 'alert': 'code and alert'})

    def test_make_answer_error(self):
        res = make_answer(400, {'error': 'code and error'})
        self.assertEqual(res, {'response': 400, 'error': 'code and error'})


if __name__ == '__main__':
    unittest.main()
