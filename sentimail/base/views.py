from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from minio import Minio
import hashlib
import os

from . models import Email
from . serializers import EmailSerializer, UploadFileSerializer



def index(request):
    return render(request, 'base/index.html')

# TODO: Test if file is already uploaded
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

    # Add email to database
    email = Email(hash=hash)
    email.save()

    # Delete the file
    os.remove(file)

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



# API

@api_view(['GET'])
def getData(request):
    #email = {'date': '2021-10-10', 'sender': 'joe' }
    emails = Email.objects.all()
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def postData(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

class UploadFileView(APIView):
    serializer_class = UploadFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file = serializer.data.get('file')
            print("File: ", file)
            fileuploaded(file)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    