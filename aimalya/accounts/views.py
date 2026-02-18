import random
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from .models import User, OTP, BusinessProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    OTPVerifySerializer, BusinessProfileSerializer, UserProfileSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP
            code = str(random.randint(100000, 999999))
            OTP.objects.create(email=user.email, code=code)
            
            # Simulated Email Sending
            print(f"OTP for {user.email}: {code}")
            
            return Response({
                "message": "User registered successfully. Please verify your email with the OTP sent.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_GATEWAY)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=OTPVerifySerializer, responses={200: str})
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            otp = OTP.objects.filter(email=email, code=code).last()
            if otp and not otp.is_expired():
                user = User.objects.get(email=email)
                user.is_verified = True
                user.save()
                otp.delete()
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_GATEWAY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_GATEWAY)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=UserLoginSerializer, responses={200: dict})
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            
            if user:
                if not user.is_verified:
                    return Response({"error": "Email not verified."}, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserProfileSerializer(user).data
                })
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_GATEWAY)

class BusinessSetupView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BusinessProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=ForgotPasswordSerializer, responses={200: dict})
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            
            if user:
                # Generate OTP
                code = str(random.randint(100000, 999999))
                OTP.objects.create(email=email, code=code)
                
                # Simulated Email Sending
                print(f"Forgot Password OTP for {email}: {code}")
                
                return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=ResetPasswordSerializer, responses={200: dict})
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            otp = OTP.objects.filter(email=email, code=code).last()
            if otp and not otp.is_expired():
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                otp.delete()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
