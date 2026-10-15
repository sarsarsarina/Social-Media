from .models import Notification


def notification_list(user):
    return(
        Notification.objects
        .filter(recipient=user)
        .select_related('actor')
        .order_by('-created_at')
    )