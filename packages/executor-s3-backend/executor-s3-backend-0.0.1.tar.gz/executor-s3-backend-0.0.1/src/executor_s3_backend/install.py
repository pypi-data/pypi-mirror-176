import sys
import json
import boto3
import daggerml
from uuid import uuid4
from daggerml._config import AWS_LOCALSTACK_ENDPOINT
from executor_s3_backend._config import GROUP, AWS_REGION, TAG


def install(store, group=GROUP, region=AWS_REGION):
    dag_name = TAG
    bucket = dag_name + '-' + uuid4().hex
    dag = daggerml.Dag.new(dag_name, group=group)
    dag.commit(dag.executor)

    print('creating bucket s3://%s/ in region %s' % (bucket, region), file=sys.stderr)
    client = boto3.client('s3', endpoint_url=AWS_LOCALSTACK_ENDPOINT)
    client.create_bucket(Bucket=bucket,
                         CreateBucketConfiguration={
                             'LocationConstraint': region})
    print('writing database to %s' % (store), file=sys.stderr)
    with open(store, 'w') as f:
        json.dump({
            'dag_name': dag.name,
            'bucket_name': bucket,
            'group': group,
            'executor': dag.executor.to_dict(),
            'secret': dag.secret,
            'pending_uploads': {},
            'uploads': {},
        }, f)
