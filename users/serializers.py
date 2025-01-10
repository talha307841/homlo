from rest_framework import serializers
from .models import CustomUser, BuyerProfile, SellerProfile, Listing, Booking

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer', 'phone_number', 'address']

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'preferences']

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'company_name', 'business_address']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_seller', 'is_buyer']

    def create(self, validated_data):
        # Create a new user instance and set the password securely
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            is_seller=validated_data.get('is_seller', False),
            is_buyer=validated_data.get('is_buyer', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'phone_number', 'address']
        read_only_fields = ['user']

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'company_name', 'phone_number', 'address']
        read_only_fields = ['user']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer']
        
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id', 'seller', 'title', 'description', 'address', 'price_per_night',
            'available_from', 'available_to', 'breakfast_included', 'lunch_included',
            'dinner_included', 'created_at', 'updated_at'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'buyer', 'listing', 'check_in', 'check_out', 'total_price', 'created_at']
        read_only_fields = ['buyer', 'total_price', 'created_at']

    def validate(self, data):
        # Ensure check-in is before check-out
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-in date must be before check-out date.")

        # Check for overlapping bookings
        listing = data['listing']
        if Booking.objects.filter(
            listing=listing,
            check_in__lt=data['check_out'],
            check_out__gt=data['check_in']
        ).exists():
            raise serializers.ValidationError("The listing is already booked for these dates.")

        return data