from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import ActivityLog, Notification, GeneralSetting
from .serializers import (
    ActivityLogSerializer, NotificationSerializer, 
    GeneralSettingSerializer, DashboardStatsSerializer
)
from django.contrib.auth import get_user_model
from accounts.models import BusinessProfile

User = get_user_model()

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=DashboardStatsSerializer)
    def get(self, request):
        data = {
            "total_users": User.objects.count(),
            "active_businesses": BusinessProfile.objects.count(),
            "total_activities": ActivityLog.objects.filter(user=request.user).count(),
        }
        return Response(data)

class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class GeneralSettingView(generics.RetrieveUpdateAPIView):
    serializer_class = GeneralSettingSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'key'

    def get_queryset(self):
        return GeneralSetting.objects.all()
