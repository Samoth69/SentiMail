from django.db import models

# Create your models here.

class UploadFile(models.Model):
    upload_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.upload_on.date()