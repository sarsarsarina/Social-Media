from django.urls import path

from .views import (
    MarkAllNotificationsAsReadView,
    MarkNotificationAsReadView,
    NotificationsListView,
    UnreadNotificationsCountView,
)

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications_list'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
    path('read-all/', MarkAllNotificationsAsReadView.as_view(), name='mark_all_notifications_read'),
    path('unread-count/', UnreadNotificationsCountView.as_view(), name='unread_notifications_count'),
]