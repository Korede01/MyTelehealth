from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MedicalRecordRequest, MedicalRecord, Notification
from .serializers import MedicalRecordRequestSerializer, MedicalRecordSerializer, NotificationSerializer
from django.core.mail import send_mail
from django.conf import settings
from patient.models import Patient

class RequestMedicalRecordView(generics.CreateAPIView):
    queryset = MedicalRecordRequest.objects.all()
    serializer_class = MedicalRecordRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, user, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(requested_by=self.request.user, patient=patient)

        # Send email notification
        subject = 'Medical Record Request Submitted'
        message = f'Hello, a new medical record request has been submitted by {self.request.user.username}.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]
        send_mail(subject, message, from_email, [to_email])

        # Send in-app notification
        notification_message = f'A new medical record request has been submitted by {self.request.user.username}.'
        Notification.objects.create(user=self.request.user, message=notification_message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MedicalRecordRequestListView(generics.ListAPIView):
    queryset = MedicalRecordRequest.objects.all()
    serializer_class = MedicalRecordRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only hospital admins should see this list
        return self.queryset.filter(status='pending')

class UploadMedicalRecordView(generics.CreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class PatientMedicalRecordsView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Patients should only see their own medical records
        return self.queryset.filter(patient__user=self.request.user)

class DownloadMedicalRecordView(generics.RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # Logic for downloading the file
        # For example, you can return a file response
        return Response({
            'id': instance.id,
            'patient': instance.patient.id,
            'record_type': instance.record_type,
            'file_url': instance.file.url,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        })

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
