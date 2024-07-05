# models.py
from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from hospital.models import Hospital

class MedicalRecordRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('entire', 'Entire'),
        ('specific_duration', 'Specific Duration')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_record_requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_record_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    uploaded_by = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='uploaded_medical_records')
    record_type = models.CharField(max_length=255)
    file = models.FileField(upload_to='medical_records/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
