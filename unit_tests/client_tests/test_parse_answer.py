import io
import unittest.mock

from common.utils import parse_answer


class TestParseAnswerFunction(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parse_answer_not_dict(self, mock_stdout=None):
        parse_answer([])
        self.assertEqual(mock_stdout.getvalue(), 'Server answer not dict\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parse_answer_no_response(self, mock_stdout=None):
        parse_answer({})
        self.assertEqual(mock_stdout.getvalue(),
                         'Answer has not "response" code\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parse_answer_ok(self, mock_stdout=None):
        parse_answer({'response': 200})
        self.assertEqual(mock_stdout.getvalue(),
                         'Server answer: 200\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parse_answer_alert(self, mock_stdout=None):
        parse_answer({'response': 400, 'alert': 'alert test'})
        self.assertEqual(mock_stdout.getvalue(),
                         'Server answer: 400\n' +
                         'Server alert message: alert test\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parse_answer_error(self, mock_stdout=None):
        parse_answer({'response': 400, 'error': 'error test'})
        self.assertEqual(mock_stdout.getvalue(),
                         'Server answer: 400\n' +
                         'Server error message: error test\n')


if __name__ == '__main__':
    unittest.main()
