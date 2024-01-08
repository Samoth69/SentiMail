import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
            if request.user.is_authenticated:
                username = request.user.username
            else:
                username = "anonymous"
            # limit 5 requests per anonymous user from the same IP address
                ip_address = request.META.get('REMOTE_ADDR')
                upload_count_key = f"upload_count_{ip_address}"

                # Check the current upload count
                current_count = cache.get(upload_count_key, 0)
                print("Upload count key: ", upload_count_key, " Current count: ", current_count)
                if current_count >= 5:
                    messages.info(request, "You have reached the maximum number of allowed uploads.")
                    return redirect(index)

                # Increment the upload count
                cache.set(upload_count_key, current_count + 1, timeout=None)
 
            print("Username: ", username)
            print("File: ", file)
            uuid = fileuploaded(file, username)
            return redirect(uploadSuccess)
        else:
            print("Serializer is not valid")
            messages.info(request, "Upload error: only .eml files are allowed")
            return redirect(index)
    else:
        form = EmailForm()
    return render(request, 'base/index.html', {'form': form})

def uploadSuccess(request):
    return render(request, 'base/uploadSuccess.html')

# TODO: Test if file is already uploaded
def fileuploaded(file, username):
    
    print("File: ", file)

    file = file[1:]

    # Generate UUID
    email_uuid = str(uuid.uuid4())
    
    print("UUID: ", email_uuid)
    # Upload the file on the object storage
    uploadFileOnObjectStorage(email_uuid, file)
    print("File uploaded on object storage")

    # Add email to database
    email = Email(uuid=email_uuid)
    email.user = username
    email.save()
    print("Email added to database")

    # Delete the file
    os.remove(file)
    print("File deleted")

    # Publish message on RabbitMQ
    publishMessage(email_uuid)
    print("Message published on RabbitMQ")

    print(f"File {email_uuid} uploaded successfully" )
    return email_uuid

# TODO: Secure this endpoint (SSL Error)   
def uploadFileOnObjectStorage(name, file):
    print("Upload file on object storage")
    minioclient = Minio(settings.MINIO_ENDPOINT,
                        settings.MINIO_ACCESS_KEY,
                        settings.MINIO_SECRET_KEY,
                        secure=False
    )
    print("Minio client created")
    
    # Make a bucket if not exists
    found = minioclient.bucket_exists(settings.MINIO_BUCKET)
    print("Bucket found: ", found)
    if not found:
        minioclient.make_bucket(settings.MINIO_BUCKET)
    print("Bucket created")
    minioclient.fput_object(settings.MINIO_BUCKET, name, file)

def publishMessage(uuid):
    ms_content = settings.RABBITMQ_MS_CONTENT
    ms_metadata = settings.RABBITMQ_MS_METADATA
    ms_attachment = settings.RABBITMQ_MS_ATTACHMENT
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        )
    )
    
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
    #channel.basic_publish(exchange='', routing_key='sentimail', body=json.dumps(uuid))
    channel.basic_publish(exchange='', routing_key=ms_metadata, body=json.dumps(uuid))
    channel.basic_publish(exchange='', routing_key=ms_content, body=json.dumps(uuid))

    
    print(" [x] Sent ", uuid, " to RabbitMQ")
    connection.close()



# API


class EmailViewset(ModelViewSet):
    http_method_names = ['get', 'patch']
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = EmailSerializer

    #Limit get result to user's emails and staff users
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Email.objects.all()
        else:
            return Email.objects.filter(user=user)
        #return Email.objects.all()

    # Limit patch method to staff users
    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "You are not allowed to edit this email"})
    

    #def get_queryset(self):
    #    return Email.objects.all()
    

class UploadFileView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UploadFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = self.request.user
        username = user.username
        if serializer.is_valid():
            serializer.save()
            file = serializer.data.get('file')
            print("File: ", file)
            uuid = fileuploaded(file, username)
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

    


""" @api_view(['GET'])
def getData(request):
    #email = {'date': '2021-10-10', 'sender': 'joe' }
    emails = Email.objects.all()
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data) """

# Patch method to add data to the database
""" @api_view(['PATCH'])
def updateResponse(request):
    serializer = EmailSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def postData(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data) """