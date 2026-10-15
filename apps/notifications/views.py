from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .paginations import NotificationListPagination
from .serializers import NotificationSerializer
from .services import get_notification_list


class NotificationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = get_notification_list(request.user)

        paginator = NotificationListPagination()
        page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)