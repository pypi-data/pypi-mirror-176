#!/usr/bin/env python3
import logging
import uvicorn
from urllib.parse import urlparse
from fastapi import FastAPI, UploadFile, Response
from executor_s3_backend import upload_funcs, get_info
from executor_s3_backend._config import DML_S3_API_ENDPOINT


logger = logging.getLogger(__name__)
app = FastAPI()


@app.get('/healthcheck')
def healthcheck():
    return {'status': 'ok'}


@app.get('/get')
def _get_info(key: str):
    info = get_info(key)
    if info is None:
        return {
            'status': 'bad',
            'error': {
                'message': 'Resource not found',
                'code': '404',
                'context': None
            }
        }
    return {'status': 'ok', 'result': info}


@app.post("/upload/{file_type}")
def post_s3_upload(file_type: str, file: UploadFile, response=Response):
    try:
        func = upload_funcs[file_type]
        res_key = func(file.file)
    except Exception as e:
        response.status_code = 403
        return {
            'status': 'bad',
            'error': {
                'message': 'There was an error uploading the file',
                'code': str(e),
                'context': None
            }
        }
    finally:
        file.file.close()
    return {
        'status': 'ok',
        'result': {
            "message": f"Successfully uploaded {file.filename}",
            'resource_key': res_key,
            'type': file_type
        }
    }


def serve(host=None, port=443):
    if host is None:
        _url = urlparse(DML_S3_API_ENDPOINT)
        host = _url.hostname
        port = _url.port or port
    return uvicorn.run(app, port=port, host=host)
