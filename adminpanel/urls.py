from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    register, HomeView, AdminListView, 
    AdminDeleteView, AdminUpdateView, AdminDetailView,
    delete_all_users, onboard_hospital, HospitalListView, HospitalDetailView, HospitalUpdateView, HospitalDeleteView)

urlpatterns = [
    
    ## -------------- HOME URL ------------- ##
    path('home/', HomeView.as_view(), name='home'),
    
    ## -------------- ADMIN URLS ------------- ##
    path('register/', register, name='register_admin'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', AdminListView.as_view(), name='admin_list'),
    path('<int:pk>/', AdminDetailView.as_view(), name='admin_detail'),
    path('update/<int:pk>/', AdminUpdateView.as_view(), name='admin_update'),
    path('delete/<int:pk>/', AdminDeleteView.as_view(), name='admin_delete'),
    path('delete/', delete_all_users, name='delete_all_users'),
    
    ## -------------- HOSPITAL URLS ------------- ##
    path('hospital/', onboard_hospital, name='onboard-hospital'),
    path('hospital/all', HospitalListView.as_view(), name='hospital-list'),
    path('hospital/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('hospital/update/<int:pk>/', HospitalUpdateView.as_view(), name='hospital-update'),
    path('hospital/delete/<int:pk>/', HospitalDeleteView.as_view(), name='hospital-delete'),
    
]
