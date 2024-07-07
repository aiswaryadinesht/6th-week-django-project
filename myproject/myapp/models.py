from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
'''Django's AbstractUser class is a built-in model provided 
by Django's authentication framework. '''
from django.contrib.auth.models import AbstractUser
# Create your models here.
# myapp/models.py

class CustomUser(AbstractUser):
    #Additional fields 
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    def __str__(self):
        return self.username
