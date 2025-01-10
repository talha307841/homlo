from django.urls import path
from .views import CreateReviewView, ListReviewsForPropertyView

urlpatterns = [
    path('create/', CreateReviewView.as_view(), name='create-review'),
    path('property/<int:property_id>/', ListReviewsForPropertyView.as_view(), name='list-reviews'),
]
