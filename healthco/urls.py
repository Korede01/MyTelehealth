from django.urls import path, include
from .view import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('admin/', include('adminpanel.urls')),
    path('hospital/', include('hospital.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls'))
]
