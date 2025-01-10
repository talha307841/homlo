from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SellerProfile, BuyerProfile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_seller:
            SellerProfile.objects.create(user=instance)
        elif instance.is_buyer:
            BuyerProfile.objects.create(user=instance)
