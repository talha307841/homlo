from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    preferences = models.TextField(blank=True)

    def __str__(self):
        return f"Buyer Profile - {self.user.username}"

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    business_address = models.TextField(blank=True)

    def __str__(self):
        return f"Seller Profile - {self.user.username}"
