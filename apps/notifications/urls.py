from django.urls import path

from .views import MarkNotificationAsReadView, NotificationsListView

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications_list'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
]