from rest_framework import serializers
from .models import MedicalRecordRequest, MedicalRecord, Notification

class MedicalRecordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecordRequest
        fields = ['id', 'patient', 'requested_by', 'request_type', 'start_date', 'end_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'requested_by', 'status', 'created_at', 'updated_at']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'uploaded_by', 'record_type', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
