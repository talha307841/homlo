from django.urls import path
from .views import CreatePropertyView, ListPropertiesView, PropertyDetailView

urlpatterns = [
    path('create/', CreatePropertyView.as_view(), name='create-property'),
    path('list/', ListPropertiesView.as_view(), name='list-properties'),
    path('<int:property_id>/', PropertyDetailView.as_view(), name='property-detail'),
]
