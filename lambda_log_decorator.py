import functools
import logging
import time
import json


def logthis_lambda_function(_func=None, level=logging.INFO, custom_message=None, omit_result=True):

    def decorator_logthis_lambda_function(func):
        @functools.wraps(func)
        def wrapper(event, context):
            start_time = time.time()
            try:
                result = _func(event, context)
                log_data = {
                    'Function': _func.__name__,
                    'Event ID': event.get("id", "unknown"),
                    'Request ID': context.aws_request_id,
                    'Execution Time': f'{time.time() - start_time} seconds',
                    'Remaining Time': f'{context.get_remaining_time_in_millis()} milliseconds',
                    'Custom Message': custom_message if custom_message else 'No custom message provided',
                    'Output': result if not omit_result else 'Output omitted, to include set omit_result=False in decorator call.'
                }
                logging.log(level, json.dumps(log_data))
                return result
            except Exception as e:
                error_log = {
                    'Function': _func.__name__,
                    'Event ID': event.get("id", "unknown"),
                    'Request ID': context.aws_request_id,
                    'Exception': str(e)
                }
                logging.error(json.dumps(error_log))
                raise e
        return wrapper

    if _func is None:
        return decorator_logthis_lambda_function
    else:
        return decorator_logthis_lambda_function(_func)