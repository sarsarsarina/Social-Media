from .models import Notification


def notification_list(user):
    return(
        Notification.objects
        .filter(recipient=user)
        .select_related('actor')
        .order_by('-created_at')
    )


def get_notification_by_id(notification_id):
    return (
        Notification.objects
        .select_related('actor')
        .filter(id=notification_id)
        .first()
    )


def unread_notifications(user):
    return Notification.objects.filter(recipient=user, is_read=False)


def unread_notifications_count(user):
    return unread_notifications(user).count()