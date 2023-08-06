import os
import json
import fcntl
from contextlib import contextmanager


TAG = 'com.daggerml.resource.s3'
GROUP = 'test0'
DML_STORE = os.getenv('DML_S3_STORE')
DML_ZONE = os.getenv('DML_ZONE')
AWS_REGION = os.getenv('AWS_REGION')
DML_S3_API_ENDPOINT = os.getenv('DML_S3_API_ENDPOINT')


if DML_S3_API_ENDPOINT is None:
    DML_S3_API_ENDPOINT = 'https://s3.{}-{}.daggerml.com'.format(DML_ZONE, AWS_REGION)


@contextmanager
def locked_open(mutate=True):
    filename = os.environ['DML_S3_STORE']
    with open(filename, 'r') as fd:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            d = json.load(fd)
            yield d
        except Exception:
            raise
        finally:
            if mutate:
                with open(filename, 'w') as f:
                    json.dump(d, f)
            fcntl.flock(fd, fcntl.LOCK_UN)


def read_data():
    with locked_open(False) as d:
        pass
    return d
