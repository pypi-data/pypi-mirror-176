# simplify

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by R Sanjeev Rao fro AWS services (c) 2022

## Examples of How To Use (Buggy Alpha Version)

Testing on Python file

```python
from simplifyaws.classes import SimplifyAWS
from simplifyaws.constants import Services
sqs_url='https://sqs.ap-southeast-1.amazonaws.com/....../sqs.fifo'

saws=SimplifyAWS(services=[Services.SQS],region="**************",aws_access_key="*********",aws_secret_key="************",secrets_name='stage/repo')


def print_data(data):
    print(data)
    return True


saws.create_sqs_loop(sqs_url=sqs_url,callback=print_data,name='Print_Loop')
saws.run_sqs_loops()
time.sleep(10)
```

Flask Example
```python
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

...........................


import time
from simplifyaws.classes import SimplifyAWS
from simplifyaws.constants import Services


def start_testing():

    sqs_url='https://sqs.ap-southeast-1.amazonaws.com/....../sqs.fifo'
    saws=SimplifyAWS(services=[Services.SQS],region="**************",aws_access_key="*********",aws_secret_key="************",  secrets_name='stage/repo')

    def print_data(data):
        print(data)
        return True

    saws.create_sqs_loop(sqs_url=sqs_url,callback=print_data,name='Print_Loop')
    saws.run_sqs_loops()

```
