from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsSuperAdmin
from .serializers import UserSerializer, HospitalSerializer
from hospital.models import Hospital

## -------------- HOME VIEW ------------- ##

class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Welcome to the Admin API'}, status=status.HTTP_200_OK)


## -------------- ADMIN VIEWS ------------- ##

## Register an admin
@api_view(['POST'])
def register(request):
    data = request.data.copy()
    data['is_staff'] = True 
    data['is_superuser'] = True
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## View all admin accounts
@permission_classes([IsAuthenticated, IsSuperAdmin])
class AdminListView(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

## View one admin account
@permission_classes([IsAuthenticated, IsSuperAdmin])
class AdminDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

## Update admin account
@permission_classes([IsAuthenticated, IsSuperAdmin])
class AdminUpdateView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_update(instance)
        return Response({'message': f'User {instance.username} updated successfully.'}, status=status.HTTP_200_OK)

## Delete one admin account
@permission_classes([IsAuthenticated, IsSuperAdmin])
class AdminDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': f'User {instance.username} has been deleted.'}, status=status.HTTP_200_OK)

## Delete all admin accounts
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def delete_all_users(request):
    User.objects.filter(is_staff=True).delete()
    return Response({'message': 'All admin users have been deleted.'}, status=status.HTTP_204_NO_CONTENT)


## -------------- HOSPITAL VIEWS ------------- ##

## Onboard Hospital    
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def onboard_hospital(request):
    serializer = HospitalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all hospitals
@permission_classes([IsAuthenticated, IsSuperAdmin])
class HospitalListView(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

# Retrieve a single hospital
@permission_classes([IsAuthenticated, IsSuperAdmin])
class HospitalDetailView(generics.RetrieveAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
# Update a hospital
@permission_classes([IsAuthenticated, IsSuperAdmin])
class HospitalUpdateView(generics.UpdateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'User updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a hospital
@permission_classes([IsAuthenticated, IsSuperAdmin])
class HospitalDeleteView(generics.DestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': f'Hospital deleted successfully.'}, status=status.HTTP_200_OK)

