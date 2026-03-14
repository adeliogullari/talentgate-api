from minio import Minio

minio_client = Minio(
    endpoint="localhost:9000",
    access_key="admin",
    secret_key="password",
    secure=False,
)

bucket = "talentgate"
object_name = "docs/AbdullahDeliogullariCV.pdf"

# Download file from MinIO
obj = minio_client.get_object(bucket, object_name)
file_bytes = obj.read()
obj.close()
obj.release_conn()
