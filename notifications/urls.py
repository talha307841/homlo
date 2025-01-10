from django.urls import path
from .views import NotificationListView, MarkNotificationAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-as-read'),
]
