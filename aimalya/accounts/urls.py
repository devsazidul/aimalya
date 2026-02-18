from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, BusinessSetupView, UserProfileView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('business-setup/', BusinessSetupView.as_view(), name='business-setup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
