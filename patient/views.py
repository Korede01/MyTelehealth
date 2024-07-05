from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer
from doctor.models import Doctor
from doctor.serializers import DoctorSerializer


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
    


class SearchDoctorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specialization = request.query_params.get('specialization')
        doctors = Doctor.objects.filter(specialization=specialization)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


