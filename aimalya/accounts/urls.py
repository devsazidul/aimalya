from django.urls import path
from .views import (
    RegisterView, VerifyOTPView, LoginView, BusinessSetupView,
    UserProfileView, ForgotPasswordView, ResetPasswordView,
    ChangePasswordView, BusinessProfileDetailView, DeleteAccountView, LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('business-setup/', BusinessSetupView.as_view(), name='business-setup'),
    path('business-profile/', BusinessProfileDetailView.as_view(), name='business-profile'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]
