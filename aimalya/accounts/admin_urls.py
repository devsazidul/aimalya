from django.urls import path
from .admin_views import (
    AdminRegisterView, AdminLoginView,
    AdminForgotPasswordView, AdminVerifyOTPView,
    AdminResetPasswordView
)

urlpatterns = [
    path('register/', AdminRegisterView.as_view(), name='admin-register'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('forgot-password/', AdminForgotPasswordView.as_view(), name='admin-forgot-password'),
    path('verify-otp/', AdminVerifyOTPView.as_view(), name='admin-verify-otp'),
    path('reset-password/', AdminResetPasswordView.as_view(), name='admin-reset-password'),
]
