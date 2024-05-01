import json
import time
import unittest
import logging
from lambda_log_decorator import logthis_lambda_function as logthis


class Context:
    aws_request_id = None

    def __init__(self):
        self.aws_request_id = '1234'

    def get_remaining_time_in_millis(self):
        return 1000


class MyTestCase(unittest.TestCase):
    def test_lambda_log_decorator_happy(self):
        logging.getLogger('root').setLevel(logging.INFO)

        @logthis
        def test_lambda_handler(event, context):
            time.sleep(0.5)
            return {
                'statusCode': 200,
                'body': json.dumps('Hello from Lambda!')
            }

        with self.assertLogs(logger='root', level='INFO') as cm:
            self.assertIsInstance(test_lambda_handler({
                "id": "1234"
            }, Context()), dict)
            self.assertEqual(len(cm.output), 1)
            self.assertIn('Function', cm.output[0])
            self.assertIn('test_lambda_handler', cm.output[0])
            self.assertIn('Request ID', cm.output[0])
            self.assertIn('Execution Time', cm.output[0])
            self.assertIn('Remaining Time', cm.output[0])
            self.assertIn('Output', cm.output[0])

    def test_lambda_log_decorator_sad(self):
        logging.getLogger('root').setLevel(logging.INFO)

        @logthis
        def test_lambda_handler(event, context):
            raise ValueError('This is an error.')

        with self.assertLogs(logger='root', level='INFO') as cm:
            self.assertRaises(ValueError, test_lambda_handler, {
                "id": "1234"
            }, Context())
            self.assertEqual(len(cm.output), 1)
            self.assertIn('Function', cm.output[0])
            self.assertIn('test_lambda_handler', cm.output[0])
            self.assertIn('Request ID', cm.output[0])
            self.assertIn('Exception', cm.output[0])


if __name__ == '__main__':
    unittest.main()
