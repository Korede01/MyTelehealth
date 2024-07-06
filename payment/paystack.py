from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from django.conf import settings

paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

def initialize_transaction(email, amount, reference, callback_url):
    response = Transaction.initialize(
        reference=reference,
        amount=amount,
        email=email,
        callback_url=callback_url,
    )
    return response

def verify_transaction(reference):
    response = Transaction.verify(reference)
    return response
