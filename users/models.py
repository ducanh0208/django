from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    sex_choice = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
