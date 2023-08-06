import json
import tarfile
import logging
import daggerml
import requests
from tempfile import NamedTemporaryFile
from pkg_resources import get_distribution, DistributionNotFound
from executor_s3._config import DML_S3_API_ENDPOINT
try:
    __version__ = get_distribution("executor-s3").version
except DistributionNotFound:
    __version__ = 'local'


logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


def _api(*args, file_=None, **kwargs):
    try:
        url = '/'.join([DML_S3_API_ENDPOINT.rstrip('/'), *args])
        if file_ is not None:
            with open(file_, 'rb') as f:
                resp = requests.post(url, files={'file': f})
        else:
            resp = requests.get(url, params=kwargs)
        if resp.status_code != 200:
            raise ApiError(f'{resp.status_code} {resp.reason}')
        resp = resp.json()
        if resp['status'] != 'ok':
            err = resp['error']
            if err['context']:
                logger.error('api error: %s', err['context'])
            raise ApiError(f'{err["code"]}: {err["message"]}')
        return resp['result']
    except KeyboardInterrupt:
        raise
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f'{e.__class__.__name__}: {str(e)}')


class S3Resource(daggerml.Resource):
    tag = 'com.daggerml.resource.s3'

    def get_s3_uri(self):
        resp = _api('get', key=self.id)
        return resp  # read_data()['uploads'].get(self.id)

daggerml.register_tag(S3Resource.tag, S3Resource)


def tar_and_upload(dag, path):
    executor = dag.load(S3Resource.tag)
    with NamedTemporaryFile('w+') as f:
        with tarfile.open(f.name, "w:gz") as tar:
            tar.add(path, arcname='/')
        resp = _api('upload', 'tar', file_=f.name)
    logger.info('got result: %s', json.dumps(resp))
    resource_key = resp['resource_key']
    upload_func = dag.from_py([executor, 'upload'])
    result = upload_func(resource_key)
    return result


def upload_file(dag, path):
    executor = dag.load(S3Resource.tag)
    resp = _api('upload', 'misc', file_=path)
    logger.info('got result: %s', json.dumps(resp))
    resource_key = resp['resource_key']
    upload_func = dag.from_py([executor, 'upload'])
    result = upload_func(resource_key)
    return result
