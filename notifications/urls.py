from django.urls import path
from .views import NotificationListView, SendNotificationView, MarkNotificationAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='list_notifications'),  # Fix root URL
    path('send/', SendNotificationView.as_view(), name='send_notification'),  # Ensure correct path
    path('<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
]

