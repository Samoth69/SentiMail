import json

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from minio import Minio
import uuid
import os
import pika
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

    # Publish message on RabbitMQ
    publishMessage(email_uuid)

    print(f"File {email_uuid} uploaded successfully" )
    return email_uuid

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

def publishMessage(uuid):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host='/',
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='sentimail')
    channel.basic_publish(exchange='', routing_key='sentimail', body=json.dumps(uuid))
    print("Json test")
    print(" [x] Sent ", uuid, " to RabbitMQ")
    connection.close()



# API

class EmailViewset(ModelViewSet):
    serializer_class = EmailSerializer
    
    def get_queryset(self):
        return Email.objects.all()


""" @api_view(['GET'])
def getData(request):
    #email = {'date': '2021-10-10', 'sender': 'joe' }
    emails = Email.objects.all()
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data) """

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
            uuid = fileuploaded(file)
            return Response(
                {
                    'uuid': uuid
                },               
                #serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    