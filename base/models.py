from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=80, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

class ResetPassword(models.Model):
    email = models.CharField(max_length=80, null=False)
    token = models.CharField(max_length=15, null=False)
    isUsed = models.BooleanField(null=False)