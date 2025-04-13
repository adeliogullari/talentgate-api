from minio import Minio
from config import get_settings

settings = get_settings()

schema = settings.minio_schema
host = settings.minio_host
port = settings.minio_port
access_key = settings.minio_root_user
secret_key = settings.minio_root_password
endpoint = f"{schema}://{host}:{port}"


def get_minio_client() -> Minio:
    return Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key)
