from rest_framework import serializers
from base.models import Email
# from ..public_api.models import UploadFile
from base.models import UploadFile

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ('file', 'upload_on')