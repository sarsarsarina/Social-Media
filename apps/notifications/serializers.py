from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_id = serializers.IntegerField(source='actor.id')
    actor_username = serializers.CharField(source='actor.username')

    class Meta:
        model = Notification
        fields = [
            'id',
            'actor_id',
            'actor_username',
            'notification_type',
            'object_id',
            'is_read',
            'created_at',
        ]