import random
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from .models import User, OTP
from .serializers import UserProfileSerializer
from .admin_serializers import (
    AdminRegistrationSerializer, AdminLoginSerializer,
    AdminForgotPasswordSerializer, AdminOTPVerifySerializer,
    AdminResetPasswordSerializer
)


class AdminRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=AdminRegistrationSerializer, responses={201: AdminRegistrationSerializer})
    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP for email verification
            code = str(random.randint(100000, 999999))
            OTP.objects.create(email=user.email, code=code)

            # Simulated Email Sending
            print(f"Admin OTP for {user.email}: {code}")

            return Response({
                "message": "Admin registered successfully. Please verify your email with the OTP sent.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "phone": user.phone,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=AdminLoginSerializer, responses={200: dict})
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_staff:
                    return Response(
                        {"error": "You are not authorized as an admin."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                if not user.is_verified:
                    return Response(
                        {"error": "Email not verified."},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserProfileSerializer(user).data
                })
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=AdminForgotPasswordSerializer, responses={200: dict})
    def post(self, request):
        serializer = AdminForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email, is_staff=True).first()

            if user:
                code = str(random.randint(100000, 999999))
                OTP.objects.create(email=email, code=code)

                # Simulated Email Sending
                print(f"Admin Forgot Password OTP for {email}: {code}")

                return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
            return Response(
                {"error": "No admin account found with this email."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminVerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=AdminOTPVerifySerializer, responses={200: dict})
    def post(self, request):
        serializer = AdminOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            otp = OTP.objects.filter(email=email, code=code).last()
            if otp and not otp.is_expired():
                user = User.objects.get(email=email)
                user.is_verified = True
                user.save()
                otp.delete()
                return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=AdminResetPasswordSerializer, responses={200: dict})
    def post(self, request):
        serializer = AdminResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']

            otp = OTP.objects.filter(email=email, code=code).last()
            if otp and not otp.is_expired():
                user = User.objects.filter(email=email, is_staff=True).first()
                if not user:
                    return Response(
                        {"error": "No admin account found with this email."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                user.set_password(new_password)
                user.save()
                otp.delete()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
