from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import HomeView, ChangePasswordView, UploadView, DoctorDetailAPIView, DoctorListCreateAPIView, PatientDetailAPIView, PatientListCreateAPIView
from medicalrecords.views import MedicalRecordRequestListView, UploadMedicalRecordView

urlpatterns = [
    
    ## -------------- HOME URL ------------- ##
    
    path('home/', HomeView.as_view(), name='home'),
    
    ## -------------- LOGIN URLS ------------- ##

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    ## -------------- PASSWORD URL ------------- ##
    
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    
    ## -------------- UPLOAD URL ------------- ##
    
    path('upload/', UploadView.as_view(), name='upload-users'),
    
    path('doctors/', DoctorListCreateAPIView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),

    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailAPIView.as_view(), name='patient-detail'),
    
    path('medical-record-requests/', MedicalRecordRequestListView.as_view(), name='medical-record-requests'),
    path('upload-medical-record/', UploadMedicalRecordView.as_view(), name='upload-medical-record'),
]


