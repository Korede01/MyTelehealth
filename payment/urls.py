# urls.py

from django.urls import path
from .views import InitializePaymentView, VerifyPaymentView

urlpatterns = [
    path('initialize-payment/', InitializePaymentView.as_view(), name='initialize-payment'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]
