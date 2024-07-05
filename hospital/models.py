from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Role(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    unique_id = models.CharField(max_length=50, unique=True)
    licensing_information = models.TextField(null=False)
    data_security_agreement = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('moderator', 'Moderator')
    ], default='admin')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


