from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomAuthenticationUser(AbstractUser):
    email = models.EmailField(unique=True)
    # By default , username is unique too.
    
    def __str__(self):
        return self.username
