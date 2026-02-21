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
            "unread_notifications": Notification.objects.filter(user=request.user, is_read=False).count(),
            "recent_activities": ActivityLogSerializer(
                ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:5],
                many=True
            ).data,
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

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: dict})
    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: dict})
    def post(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"message": f"{updated} notifications marked as read."}, status=status.HTTP_200_OK)

class GeneralSettingView(generics.RetrieveUpdateAPIView):
    serializer_class = GeneralSettingSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'key'

    def get_queryset(self):
        return GeneralSetting.objects.all()
