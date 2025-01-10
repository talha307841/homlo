from django.urls import path
from .views import SellerDashboardView

urlpatterns = [
    path('seller-dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
]
