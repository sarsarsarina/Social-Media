from django.urls import path

from .views import (
    MarkAllNotificationsAsReadView,
    MarkNotificationAsReadView,
    NotificationsListView,
)

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications_list'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
    path('read-all/', MarkAllNotificationsAsReadView.as_view(), name='mark_all_notifications_read'),
]