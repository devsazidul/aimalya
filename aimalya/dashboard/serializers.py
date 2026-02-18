from rest_framework import serializers
from .models import ActivityLog, Notification, GeneralSetting
from django.contrib.auth import get_user_model
from accounts.models import BusinessProfile

User = get_user_model()

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']

class GeneralSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSetting
        fields = ['id', 'key', 'value', 'description']

class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_businesses = serializers.IntegerField()
    total_activities = serializers.IntegerField()

    def get_stats(self):
        return {
            "total_users": User.objects.count(),
            "active_businesses": BusinessProfile.objects.count(),
            "total_activities": ActivityLog.objects.count(),
        }
