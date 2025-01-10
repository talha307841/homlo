from django.urls import path
from .views import CreateBookingView, ListBookingsForUserView

urlpatterns = [
    path('create/', CreateBookingView.as_view(), name='create-booking'),
    path('my-bookings/', ListBookingsForUserView.as_view(), name='list-bookings'),
]
