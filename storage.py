from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client

from desert import settings, constant
from desert.utils import generate_filename

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY
region = settings.REGION
bucket = settings.BUCKET
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)
client = CosS3Client(config)


@deconstructible
class TencentStorage(Storage):
    def save(self, name, content, max_length=None):
        client.put_object(
            Bucket=bucket,
            Key='custom_path/' + name,
            Body=content.read()
        )
        return name

    def url(self, name):
        file_url = client.get_presigned_url(
            Method=constant.GET_METHOD,
            Bucket=bucket,
            Key='custom_path/' + name,
            Expired=120
        )
        return str(file_url)

    def generate_filename(self, filename):
        return generate_filename(filename, '.custom_extensions')

    def delete(self, name):
        client.delete_object(bucket, name)
        return name
