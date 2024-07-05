from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Appointment, DoctorAvailability
from .serializers import AppointmentSerializer, DoctorAvailabilitySerializer, AllAppointmentsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from core.utils import get_doctor_availability
from doctor.models import Doctor
from patient.models import Patient


class DoctorAvailabilityCreateView(generics.CreateAPIView):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        try:
            doctor = Doctor.objects.get(user=user)  # Get the Doctor instance associated with the User
        except Doctor.DoesNotExist:
            raise ValidationError("The user is not associated with any doctor.")
        
        serializer.save(doctor=doctor)

class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AllAppointmentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            raise ValidationError("The user is not associated with any doctor.")

        return Appointment.objects.filter(doctor=doctor)

class AppointmentView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the logged-in patient
        patient = Patient.objects.get(user=self.request.user)
        return self.queryset.filter(patient=patient)

    def perform_create(self, serializer):
        doctor_id = self.kwargs['doctor_id']
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            raise ValidationError("The selected doctor does not exist.")

        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        availability = DoctorAvailability.objects.filter(
            doctor=doctor, date=date,
            start_time__lte=time, end_time__gte=time
        ).exists()

        if not availability:
            raise ValidationError("The selected time slot is not available.")

        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise ValidationError("The selected time slot is already booked.")

        appointment = serializer.save(doctor=doctor, patient=Patient.objects.get(user=self.request.user))

        send_mail(
            'Appointment Confirmation',
            f'Your appointment with Dr. {doctor.user.username} on {date} at {time} has been confirmed.',
            'erinlekorede@gmail.com',
            [self.request.user.email],
            fail_silently=False,
        )

class AvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id, date):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=404)
        
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        availabilities, recurring_slots = get_doctor_availability(doctor, date)

        response_data = []

        for availability in availabilities:
            response_data.append({
                'start_time': availability.start_time,
                'end_time': availability.end_time
            })

        for slot in recurring_slots:
            response_data.append(slot)

        return Response(response_data)