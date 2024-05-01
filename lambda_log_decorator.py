import functools
import logging
import time
import json


def logthis_lambda_function(_func=None, *, level=logging.INFO, custom_message=None, omit_result=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, context):
            start_time = time.time()
            event_id = event.get("id", "unknown") if isinstance(event, dict) else "non-dict event"
            request_id = getattr(context, 'aws_request_id', 'unknown_request_id')

            try:
                result = func(event, context)
                log_data = {
                    'Function': func.__name__,
                    'Event ID': event_id,
                    'Request ID': request_id,
                    'Execution Time': f'{time.time() - start_time} seconds',
                    'Remaining Time': f'{context.get_remaining_time_in_millis()} milliseconds',
                    'Custom Message': custom_message if custom_message else 'No custom message provided',
                    'Output': result if not omit_result else 'Output omitted'
                }
                logging.log(level, json.dumps(log_data))
                return result
            except Exception as e:
                error_log = {
                    'Function': func.__name__,
                    'Event ID': event_id,
                    'Request ID': request_id,
                    'Execution Time': f'{time.time() - start_time} seconds',
                    'Exception': str(e),
                    'Custom Message': custom_message if custom_message else 'No custom message provided'
                }
                logging.error(json.dumps(error_log))
                raise e

        return wrapper

    return decorator(_func) if _func is not None else decorator
