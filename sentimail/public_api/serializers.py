from rest_framework import serializers
from base.models import Email
from . models import UploadFile

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ('file', 'upload_on')