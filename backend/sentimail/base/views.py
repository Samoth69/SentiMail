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


""" global rabbit_connection
global rabbit_channel 
rabbit_connection, rabbit_channel = None, None

def connectRabbitMQ():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="sentimail", exchange_type='direct')
    #channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
    return connection, channel
"""

def index(request):

    if request.method == 'POST':
        serializer_class = UploadFileSerializer
        parser_classes = (MultiPartParser, FormParser)
        serializer = serializer_class(data=request.FILES)
        if serializer.is_valid():
            # Rename the file and save it
            serializer.validated_data['file'].name = str(uuid.uuid4()) + ".eml"
            serializer.save()
            file = serializer.data.get('file')

            # Rename the file
            
            print("File name: ", file)

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
            uuid_file = fileuploaded(file, username)
            #return redirect(uploadSuccess)
            return redirect(result, uuid=uuid_file)
        else:
            print("Serializer is not valid")
            messages.info(request, "Upload error: only .eml files are allowed")
            return redirect(index)
    else:
        form = EmailForm()
    return render(request, 'base/index.html', {'form': form})

def uploadSuccess(request):
    return render(request, 'base/uploadSuccess.html')

def api_doc(request):
    return render(request, 'base/api_doc.html')

def historic(request):
    # Get all emails from user
    user = request.user

    analysis = Email.objects.filter(user=user)

    # Si pas de données, afficher un message

    return render(request, 'base/historic.html', {'analysis': analysis})

def result(request, uuid):
    email = Email.objects.get(uuid=uuid)

    env = os.getenv("BACKEND_HOST", "127.0.0.1:8000")

    # Passer une variable à la vue pour pouvoir l'utiliser dans le template
    return render(request, 'base/result.html', {'email': email, 'env': env})

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
    """ global rabbit_connection
    global rabbit_channel
    if rabbit_connection is None:
        print("Connecting to RabbitMQ")
        rabbit_connection, rabbit_channel = connectRabbitMQ() """

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host=settings.RABBITMQ_VHOST,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
            )
        )
    channel = connection.channel()
    channel.exchange_declare(exchange="sentimail", exchange_type='direct')
    ms_content = settings.RABBITMQ_MS_CONTENT
    ms_metadata = settings.RABBITMQ_MS_METADATA
    ms_attachment = settings.RABBITMQ_MS_ATTACHMENT

    #channel.basic_publish(exchange='', routing_key='sentimail', body=json.dumps(uuid))

    channel.basic_publish(exchange='sentimail', routing_key='all', body=json.dumps(uuid))

    #rabbit_channel.basic_publish(exchange='', routing_key=ms_metadata, body=json.dumps(uuid))
    #rabbit_channel.basic_publish(exchange='', routing_key=ms_content, body=json.dumps(uuid))

    
    print(" [x] Sent ", uuid, " to RabbitMQ")
    connection.close()

def is_ready(uuid_analysis):
    """Check if the analysis is ready
    :param uuid_analysis: uuid of the analysis
    :return: True if the analysis is ready, False if not
    """
    # Get the analysis from the database
    analysis = Email.objects.get(uuid=uuid_analysis)
    status_metadata = False
    status_content = False
    status_attachment = False
    if analysis.responseMetadataIp != "":
        status_metadata = True
    if analysis.responseContentLinks != "":
        status_content = True
    if analysis.responseAttachmentHash != "":
        status_attachment = True
    
    if status_metadata and status_content and status_attachment:
        score_calculator(uuid_analysis)
    
    analysis = Email.objects.get(uuid=uuid_analysis)
    return analysis.isReady

def score_calculator(uuid_analysis):
    """Calculate the score of the email
    :param uuid_analysis: uuid of the analysis
    :return: score of the email in percentage
    """
    score = 0

    # Get the analysis from the database
    analysis = Email.objects.get(uuid=uuid_analysis)

    metadata_ip = analysis.responseMetadataIp
    metadata_domain = analysis.responseMetadataDomain
    metadata_spf = analysis.responseMetadataSPF
    content_links = analysis.responseContentLinks
    content_spelling = analysis.responseContentSpelling
    content_keywords = analysis.responseContentKeywords
    content_typosquatting = analysis.responseContentTyposquatting
    content_character = analysis.responseContentCharacter
    attachment_hash = analysis.responseAttachmentHash
    attachment_filetype = analysis.responseAttachmentFiletype

    # Calculate the score
    
    if metadata_ip == "Malicious":
        score += 10
    if metadata_domain == "Malicious":
        score += 10
    if metadata_spf == "Malicious":
        score += 10
   
    if content_links == "Malicious":
        score += 10
    if content_spelling == "Malicious":
        score += 10
    if content_keywords == "Phishing":
        score += 10
    elif content_keywords == "Spam":
        score += 5
    if content_typosquatting == "Malicious":
        score += 10
    if content_character == "Malicious":
        score += 10
    
    if attachment_hash == "Malicious":
        score += 10
    if attachment_filetype == "Malicious":
        score += 10

    if attachment_hash == "No attachment":
        score = 100 * score / 80
    
    # Set the score and isReady in the database
    analysis.score = score
    analysis.isReady = True
    analysis.save()

    print("Score for ", uuid_analysis, ": ", score)
    return score
    




# API
# Return analysis result for anonymous users

class EmailViewsetResult(ModelViewSet):
    http_method_names = ['get']

    serializer_class = EmailSerializer

    def get_queryset(self):
        return Email.objects.all().filter(user="anonymous")


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
            response = super().update(request, *args, **kwargs)
            is_ready(kwargs['pk'])
            return response
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
            serializer.validated_data['file'].name = str(uuid.uuid4()) + ".eml"
            serializer.save()
            file = serializer.data.get('file')
            print("File: ", file)
            uuid_file = fileuploaded(file, username)
            return Response(
                {
                    'uuid': uuid_file
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