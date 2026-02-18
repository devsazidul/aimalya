from django.urls import path
from .views import (
    DashboardStatsView, ActivityLogListView, 
    NotificationListView, GeneralSettingView
)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('activities/', ActivityLogListView.as_view(), name='activity-logs'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('settings/<str:key>/', GeneralSettingView.as_view(), name='general-setting'),
]
