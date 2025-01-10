from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,  RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, BuyerProfile, SellerProfile
from .serializers import (CustomUserSerializer, BuyerProfileSerializer, SellerProfileSerializer,
                          UserRegistrationSerializer, UserDetailSerializer, ListingSerializer, BookingSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import CustomUser, Booking
from notifications.services import create_notification

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.buyer_profile
            serializer = BuyerProfileSerializer(profile)
            return Response(serializer.data)
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=404)

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile)
            return Response(serializer.data)
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller profile not found."}, status=404)
        



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Optionally, include user details in the response
        user = self.get_user(request.data.get('username'))
        if user:
            response.data.update({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_seller': user.is_seller,
                    'is_buyer': user.is_buyer,
                }
            })
        return response

    def get_user(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_seller": user.is_seller,
                    "is_buyer": user.is_buyer
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.buyer_profile
            serializer = BuyerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = request.user.buyer_profile
            serializer = BuyerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller profile not found."}, status=status.HTTP_404_NOT_FOUND)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.buyer_profile
            serializer = BuyerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = request.user.buyer_profile
            serializer = BuyerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller profile not found."}, status=status.HTTP_404_NOT_FOUND)

class ListingListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListingSerializer



class BookingListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_buyer:
            return Booking.objects.filter(buyer=self.request.user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
        create_notification(
                user=property.owner,  # Notify the seller
                message=f"You have a new booking for {property.name} from {self.request.user.username}."
            )

class BookingDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_buyer:
            return Booking.objects.filter(buyer=self.request.user)
        return Booking.objects.none()