from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import HomeView, ChangePasswordView, UploadView, DoctorDetailAPIView, DoctorListCreateAPIView, PatientDetailAPIView, PatientListCreateAPIView, AppointmentDetailView, AppointmentListCreateView


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
    
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
]


