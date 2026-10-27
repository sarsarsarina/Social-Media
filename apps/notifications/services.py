from rest_framework.exceptions import NotFound

from .selectors import (
    get_notification_by_id,
    notification_list,
    unread_notifications,
    unread_notifications_count,
)


def get_notification_list(user):
    return notification_list(user)


def mark_notification_as_read(user, notification_id):
    notification = get_notification_by_id(notification_id)

    if not notification or notification.recipient_id != user.id:
        raise NotFound("Notification not found")

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    return notification


def mark_all_notifications_as_read(user):
    updated_count = unread_notifications(user).update(is_read=True)
    return updated_count


def get_unread_notifications_count(user):
    return unread_notifications_count(user)