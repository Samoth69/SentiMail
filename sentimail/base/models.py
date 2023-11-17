from django.db import models

# Create your models here.

class Email(models.Model):
    hash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default="anonymous")