from .selectors import notification_list


def get_notification_list(user):
    return notification_list(user)