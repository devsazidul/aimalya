from django.urls import path
from .views import (
    DashboardStatsView, ActivityLogListView, 
    NotificationListView, GeneralSettingView,
    MarkNotificationReadView, MarkAllNotificationsReadView
)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('activities/', ActivityLogListView.as_view(), name='activity-logs'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),
    path('settings/<str:key>/', GeneralSettingView.as_view(), name='general-setting'),
]
