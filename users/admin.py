from django.contrib import admin
from .models import CustomUser, BuyerProfile, SellerProfile

admin.site.register(CustomUser)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
