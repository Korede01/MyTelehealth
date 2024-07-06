# views.py
from datetime import timezone, timedelta
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment, Subscription
from .serializers import PaymentSerializer, SubscriptionSerializer
from .paystack import initialize_transaction, verify_transaction

class InitializePaymentView(generics.CreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        email = request.user.email
        amount = request.data.get('amount')
        reference = request.data.get('reference')
        callback_url = request.data.get('callback_url')
        
        response = initialize_transaction(email, amount, reference, callback_url)
        return Response(response, status=status.HTTP_200_OK)

class VerifyPaymentView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        response = verify_transaction(reference)
        
        if response['status']:
            payment = Payment.objects.create(
                user=request.user,
                reference=reference,
                amount=response['data']['amount'] / 100,
                status='success',
            )
            # Handle subscription activation here if necessary
            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        response = verify_transaction(reference)
        
        if response['status']:
            payment = Payment.objects.create(
                user=request.user,
                reference=reference,
                amount=response['data']['amount'] / 100,
                status='success',
            )

            # Activate subscription
            plan = request.query_params.get('plan')
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=30)  # Assuming a monthly subscription
            
            Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
            )
            
            return Response({'message': 'Payment successful and subscription activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

