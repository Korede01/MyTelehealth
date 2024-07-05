from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, CSVUploadSerializer
from doctor.models import Doctor
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from patient.serializers import PatientSerializer


## -------------- HOME VIEW ------------- ##

class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Welcome to the Hospital API'}, status=status.HTTP_200_OK)

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

## -------------- UPLOAD VIEW ------------- ##

class UploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        hospital = request.user.hospital
        serializer = CSVUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                print(f"Processing CSV file: {file.name}")  # Debug statement
                serializer.process_csv(file, hospital)
            elif file.name.endswith('.xml'):
                print(f"Processing XML file: {file.name}")  # Debug statement
                serializer.process_xml(file, hospital)
            else:
                return Response({"detail": "Unsupported file format."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"detail": "File processed successfully."}, status=status.HTTP_200_OK)
        print(f"Serializer errors: {serializer.errors}")  # Debug statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

class DoctorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

class PatientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

class PatientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


