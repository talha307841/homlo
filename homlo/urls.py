from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/users/', include('users.urls')),  # Routes for the users app
    path('api/payments/', include('payments.urls')), 
    path('api/dashboard/', include('dashboard.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/properties/', include('properties.urls')),


]
