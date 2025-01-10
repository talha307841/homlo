from django.urls import path
from .views import UserDetailView, BuyerProfileView, SellerProfileView, CustomTokenObtainPairView, UserRegistrationView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('buyer-profile/', BuyerProfileView.as_view(), name='buyer-profile'),
    path('seller-profile/', SellerProfileView.as_view(), name='seller-profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
