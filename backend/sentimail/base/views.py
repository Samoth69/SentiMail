from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from minio import Minio
import uuid
import os
from . emailform import EmailForm

from . models import Email
from . serializers import EmailSerializer, UploadFileSerializer

def index(request):

    if request.method == 'POST':
        serializer_class = UploadFileSerializer
        parser_classes = (MultiPartParser, FormParser)
        serializer = serializer_class(data=request.FILES)
        if serializer.is_valid():
            serializer.save()
            file = serializer.data.get('file')
            print("File: ", file)
            fileuploaded(file)
            return redirect(uploadSuccess)
    else:
        form = EmailForm()
    return render(request, 'base/index.html', {'form': form})
    #return render(request, 'base/index.html')
    """ if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file = form.path()
            print("File: ", file)
            fileuploaded(file)
            return redirect(uploadSuccess) """

def uploadSuccess(request):
    return render(request, 'base/uploadSuccess.html')

# TODO: Test if file is already uploaded
def fileuploaded(file):
    
    print("File: ", file)

    file = file[1:]

    # Generate UUID
    email_uuid = str(uuid.uuid4())
    
    # Upload the file on the object storage
    uploadFileOnObjectStorage(email_uuid, file)

    # Add email to database
    email = Email(uuid=email_uuid)
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

    