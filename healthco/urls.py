from django.contrib import admin
from django.urls import path, include
from .view import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home'),
    path('admins/', include('adminpanel.urls')),
    path('hospital/', include('hospital.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls'))
]
