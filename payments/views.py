import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Payment
from users.models import Booking
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            booking_id = request.data.get('booking_id')
            if not booking_id:
                return Response({"error": "Booking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            booking = Booking.objects.get(id=booking_id, buyer=request.user)
            if Payment.objects.filter(booking=booking).exists():
                return Response({"error": "Payment already exists for this booking"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a Stripe Payment Intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(booking.total_price * 100),  # Amount in cents
                currency="usd",  # Adjust currency as needed
                metadata={"booking_id": booking.id}
            )

            # Save the payment record in the database
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                stripe_payment_intent_id=payment_intent['id'],
                status='PENDING'
            )

            return Response({
                "client_secret": payment_intent['client_secret'],
                "payment_id": payment.id
            }, status=status.HTTP_201_CREATED)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StripePaymentConfirmationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            if not payment_id:
                return Response({"error": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            payment = Payment.objects.get(id=payment_id, booking__buyer=request.user)
            payment_intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)

            if payment_intent['status'] == 'succeeded':
                payment.status = 'COMPLETED'
                payment.save()
                return Response({"message": "Payment completed successfully"}, status=status.HTTP_200_OK)
            else:
                payment.status = 'FAILED'
                payment.save()
                return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
