import os

from minio import Minio
#from file import *
from dotenv import load_dotenv
import tempfile
import custom_logger

logger = custom_logger.getLogger("bucket_call")

# Create client with access key and secret key with specific region.

load_dotenv()

def bucket_call(id_file):
    client = Minio(
        os.getenv('MINIO_ENDPOINT'),
        access_key= os.getenv('MINIO_ACCESS_KEY'),
        secret_key= os.getenv('MINIO_SECRET_KEY'),
        secure=False,
    )

    fi = tempfile.mkstemp(prefix="ms-content-")
    logger.debug(fi)
    fi = fi[1]
    logger.debug("temporary file name %s", fi)

    # Download data of an object.
    client.fget_object(os.getenv("MINIO_BUCKET", "sentimail"), id_file,
                    fi)

    return fi




