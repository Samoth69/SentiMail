from django.db import models

# Create your models here.

class Email(models.Model):
    uuid = models.CharField(max_length=100, primary_key=True) # hash a indéxer ou unique (contrainte)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default="anonymous")
    isReady = models.BooleanField(default=False)
    responseMetadataIp = models.CharField(max_length=100, default="")
    responseMetadataDomain = models.CharField(max_length=100, default="")

class UploadFile(models.Model):
    upload_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    uuid = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.upload_on.date()