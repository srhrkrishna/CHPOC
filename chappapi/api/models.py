from django.db import models

# Create your models here.
class Video(models.Model):
    fileData = models.FileField(upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)