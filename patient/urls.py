from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)
from .views import HomeView, ChangePasswordView, SearchDoctorView
from appointment.views import AvailableSlotsView, AppointmentView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('search-doctor/', SearchDoctorView.as_view(), name='search-doctor'),
    path('<int:doctor_id>/available-slots/<str:date>/', AvailableSlotsView.as_view(), name='available-slots'),
    path('book-appointments/<int:doctor_id>/', AppointmentView.as_view(), name='doctor-appointments'),
]
