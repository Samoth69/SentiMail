from django.db import models

# Create your models here.

class Email(models.Model):
    uuid = models.CharField(max_length=100) # hash a indéxer ou unique (contrainte)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default="anonymous")

class UploadFile(models.Model):
    upload_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    uuid = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.upload_on.date()