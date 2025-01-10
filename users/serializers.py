from rest_framework import serializers
from .models import CustomUser, BuyerProfile, SellerProfile

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