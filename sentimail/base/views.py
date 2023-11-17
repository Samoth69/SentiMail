from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from . models import Email
from minio import Minio
import hashlib
import os

def index(request):
    return render(request, 'base/index.html')

def fileuploaded(file):
    
    print("File: ", file)
    file = file[1:]
    
    # Generate the hash (SHA-256) of the file
    with open(file, 'rb') as f:
        data = f.read()
        hash = hashlib.sha256(data).hexdigest()
        print("Hash: ", hash)
    
    # Upload the file on the object storage
    uploadFileOnObjectStorage(hash, file)

    # TODO: Add email to database
    email = Email(hash=hash)
    email.save()

    print("File uploaded")

# TODO: Secure this endpoint (SSL Error)   
def uploadFileOnObjectStorage(name, file):
    minioclient = Minio(settings.MINIO_ENDPOINT,
                        settings.MINIO_ACCESS_KEY,
                        settings.MINIO_SECRET_KEY,
                        secure=False
    )
    # Make a bucket if not exists
    found = minioclient.bucket_exists("sentimail")
    if not found:
        minioclient.make_bucket("sentimail")
    minioclient.fput_object("sentimail", name, file)