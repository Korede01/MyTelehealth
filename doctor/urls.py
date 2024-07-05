from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import HomeView, ChangePasswordView, DoctorAvailabilityView, DoctorAppointmentsView


urlpatterns = [
    
    ## -------------- HOME URL ------------- ##
    
    path('home/', HomeView.as_view(), name='home'),
    
    ## -------------- LOGIN URLS ------------- ##

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    ## -------------- PASSWORD URL ------------- ##
    
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('availability/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('appointments/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    
]