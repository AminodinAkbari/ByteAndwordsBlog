from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.db import models
from django.contrib.auth.models import AbstractUser

def avatar_upload_to(instance , filename):
    return f"avatars/{instance.id}/{filename}"

class CustomAuthenticationUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length = 250, blank=True ,null=True)
    avatar = models.ImageField(upload_to=avatar_upload_to , blank=True , null=True)

    def __str__(self):
        return self.username
