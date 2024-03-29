from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Email(models.Model):
    uuid = models.CharField(max_length=100, primary_key=True) # hash a indéxer ou unique (contrainte)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default="anonymous")
    isReady = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    verdict = models.CharField(max_length=100, default="")
    sender = models.CharField(max_length=100, default="")
    recipient = models.CharField(max_length=100, default="")
    subject = models.CharField(max_length=100, default="")
    delivery_date = models.CharField(max_length=100, default="") 
    responseMetadataIp = models.CharField(max_length=100, default="")
    responseMetadataDomain = models.CharField(max_length=100, default="")
    responseMetadataSPF = models.CharField(max_length=100, default="")
    responseMetadataDKIM = models.CharField(max_length=100, default="")
    responseContentLinks = models.CharField(max_length=100, default="")
    responseContentSpelling = models.CharField(max_length=100, default="")
    responseContentKeywords = models.CharField(max_length=100, default="")
    responseContentTyposquatting = models.CharField(max_length=100, default="")
    responseContentCharacter = models.CharField(max_length=100, default="")
    responseAttachmentHash = models.CharField(max_length=100, default="")
    responseAttachmentFiletype = models.CharField(max_length=100, default="")


class UploadFile(models.Model):
    upload_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['eml'])])
    uuid = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.upload_on.date()