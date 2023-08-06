import os


DML_ZONE = os.getenv('DML_ZONE')
DML_REGION = os.getenv('DML_REGION')
DML_S3_API_ENDPOINT = os.getenv('DML_S3_API_ENDPOINT')


if DML_S3_API_ENDPOINT is None:
    DML_S3_API_ENDPOINT = 'https://s3.{}-{}.daggerml.com'.format(DML_ZONE, DML_REGION)
