from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginations import NotificationListPagination
from .serializers import NotificationSerializer
from .services import (
    get_notification_list,
    mark_all_notifications_as_read,
    mark_notification_as_read,
)


class NotificationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = get_notification_list(request.user)

        paginator = NotificationListPagination()
        page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        notification = mark_notification_as_read(request.user, notification_id)
        serializer = NotificationSerializer(instance=notification)

        return Response(serializer.data)


class MarkAllNotificationsAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated_count = mark_all_notifications_as_read(request.user)

        return Response(
            {"message": "All notifications marked as read.", "updated_count": updated_count},
            status=status.HTTP_200_OK
        )

    