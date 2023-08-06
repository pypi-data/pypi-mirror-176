# aiosqs

Python asynchronous and lightweight SQS client.


## Why aiosqs?

Main problem of `botocore` and `aiobotocore` is huge memory and CPU consumption:
- https://github.com/boto/boto3/issues/1670
- https://github.com/aio-libs/aiobotocore/issues/940
- https://github.com/aio-libs/aiobotocore/issues/970

Also aiobotocore itself is a transition of botocore to async interface without any optimizations.

So the goal of different library is to provide fast and optimal access to SQS for Python projects, e.g. when you need a high-load queue consumer or high-load queue producer written in Python.


## How to use

Basic example for all cases:

```python
client = SQSClient(
    logger=logger,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    host=host,
)

response = await self.client.get_queue_url(queue_name=queue_name)
queue_url = response["QueueUrl"]

response = await client.send_message(
    queue_url=queue_url,
    message_body=json.dumps({"demo": 1, "key": "value"}),
    delay_seconds=0,
)
print(response)

response = await client.receive_message(
    queue_url=queue_url,
    max_number_of_messages=1,
    visibility_timeout=30,
)
if response:
    message = response["Message"][0]
```
