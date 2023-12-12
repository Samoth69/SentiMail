import os

from minio import Minio
from file import *
from dotenv import load_dotenv


# Create client with access key and secret key with specific region.

load_dotenv()

def bucket_call(id_file):
    client = Minio(
        os.getenv('MINIO_ENDPOINT'),
        access_key= os.getenv('MINIO_ACCESS_KEY'),
        secret_key= os.getenv('MINIO_SECRET_KEY'),
        secure=False,
    )

    # Download data of an object.
    client.fget_object(os.getenv("MINIO_BUCKET", "sentimail"), id_file,
                       id_file)




