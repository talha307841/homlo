from django.urls import path
from .views import StripePaymentIntentView, StripePaymentConfirmationView

urlpatterns = [
    path('stripe/create-payment-intent/', StripePaymentIntentView.as_view(), name='stripe-create-payment-intent'),
    path('stripe/confirm-payment/', StripePaymentConfirmationView.as_view(), name='stripe-confirm-payment'),
]
