from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=80, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)