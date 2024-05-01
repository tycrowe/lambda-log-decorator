# Project Title: LambdaLogDecorator

## Project Summary:
The LambdaLogDecorator is a simple Python decorator that logs the input and output of a function.  I find it useful for 
quickly attaching common logging to a python-based AWS lambda function.

## Objective:
- To provide a simple Python decorator that logs the input and output of a function.

## Usage
This is meant for Python based AWS Lambda functions only.

To use the LambdaLogDecorator, simply import the `log_decorator` function from the `lambda_log_decorator.py` file and
decorate the function you want to log. Here is an example:

```python
import json
import logging
from lambda_log_decorator import logthis_lambda_function as logthis

@logthis(level=logging.DEBUG)
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

I would recommend keeping the decorator in a lambda layer so that you can easily attach it to any lambda function you want!

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute this code as you see fit. 
See the [LICENSE.md](LICENSE.md) file for more details.

## About Me
My name is Tyler Crowe, I do that cool programming stuff. Here is my website: [tycrowe.com](https://tycrowe.com)