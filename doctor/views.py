import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer
from .models import Doctor



## -------------- HOME VIEW ------------- ##

class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Welcome to the Doctor API'}, status=status.HTTP_200_OK)

## -------------- CHANGE PASSWORD VIEW ------------- ##

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def retrieve_calendly_user_info(user, access_token):
    doctor = Doctor.objects.get(user=user)
    calendly_url = "https://api.calendly.com/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(calendly_url, headers=headers)
    if response.status_code == 200:
        calendly_data = response.json()
        doctor.calendly_user = calendly_data['resource']['uri']
        doctor.save()
        return redirect("success_page")
    else:
        return redirect("error_page")

class DoctorAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        doctor = request.user.doctor
        availability_data = request.data.get('availability')
        # Save availability data to Calendly
        calendly_url = f"https://api.calendly.com/users/me/availability"
        headers = {
            "Authorization": f"Bearer {settings.CALENDLY_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(calendly_url, headers=headers, json=availability_data)
        if response.status_code == 201:
            return Response({"message": "Availability updated successfully"}, status=201)
        else:
            return Response({"error": "Failed to update availability"}, status=response.status_code)

class DoctorAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = request.user.doctor
        calendly_url = f"https://api.calendly.com/scheduled_events?user={doctor.calendly_user}"
        headers = {
            "Authorization": f"Bearer {settings.CALENDLY_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(calendly_url, headers=headers)
        appointments = response.json()
        return Response(appointments)


