import os
import boto3
import logging
from uuid import uuid4
from hashlib import md5
from daggerml import Dag, Resource
from tempfile import NamedTemporaryFile
from subprocess import PIPE, run as run_shell
from daggerml._config import AWS_LOCALSTACK_ENDPOINT
from executor_s3_backend._config import read_data, locked_open, GROUP, TAG


logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, os.getenv('DML_LOG_LEVEL', 'INFO')))

my_dir = os.path.dirname(os.path.realpath(__file__))


def upload_tar(fio):
    bucket = read_data()['bucket_name']
    resource_id = uuid4().hex
    with NamedTemporaryFile('wb') as f:
        while contents := fio.read(1024 * 1024):
            f.write(contents)
        f.seek(0)
        proc = run_shell([f'{my_dir}/hash-tar.sh', f.name], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            return False
        md5 = proc.stdout
        assert md5 is not None, 'bad md5sum'
        key = f'tar/{md5.decode()}.tar'
        client = boto3.client('s3', endpoint_url=AWS_LOCALSTACK_ENDPOINT)
        client.upload_file(f.name, bucket, key)
    s3_path = f's3://{bucket}/{key}'
    with locked_open() as d:
        d['pending_uploads'][resource_id] = s3_path
    return resource_id


def upload_misc(fio):
    # fio is a io object (like `f` in `with open(...) as f:`)
    # FIXME: add check for file size and use multipart uploads
    bucket = read_data()['bucket_name']
    key = f'unique-objs/{uuid4().hex}'
    resource_id = uuid4().hex
    s3_path = f's3://{bucket}/{key}'
    client = boto3.client('s3', endpoint_url=AWS_LOCALSTACK_ENDPOINT)
    client.put_object(Bucket=bucket, Key=key, Body=fio)
    with locked_open() as d:
        d['pending_uploads'][resource_id] = s3_path
    return resource_id


upload_funcs = {
    'tar': upload_tar,
    'misc': upload_misc
}


def get_info(key):
    return read_data()['uploads'].get(key)


def get_run_job():
    data = read_data()
    executor = Resource.from_dict(data['executor'])
    secret = data['secret']
    exec_dag = Dag.from_claim(executor, secret, 1000, GROUP)
    if exec_dag is None:
        return False
    with exec_dag:
        assert exec_dag.expr[0][1].to_py() == 'upload'
        upload_key = exec_dag.expr[1].to_py()
        with locked_open() as data:
            assert upload_key in data['pending_uploads']
            resid = data['pending_uploads'].pop(upload_key)
            resource_key = md5(resid.encode()).hexdigest()
            data['uploads'][resource_key] = resid
        exec_dag.commit(Resource(resource_key, executor, tag=TAG))
    return True
