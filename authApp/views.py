from rest_framework.response import Response
from rest_framework import status
from . import models
from django.contrib.auth import authenticate
from . import serializers
from . import renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
    renderer_classes = [renderers.UserRenderers]
    def post(self, request, format=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = get_tokens_for_user(user=user)
            return Response({"msg": "Registration Successful..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOTP(APIView):
    renderer_classes = [renderers.UserRenderers]

    def post(self, request, format=None):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = models.User.objects.get(email=email)
                if user.otp == otp:
                    user.is_verified = True
                    user.otp = None
                    user.save()
                    token = get_tokens_for_user(user)
                    return Response({'token': token, 'msg': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'errors': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            except models.User.DoesNotExist:
                return Response({'errors': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    renderer_classes = [renderers.UserRenderers]

    def post(self, request, format=None):
        print(request.data)
        serializer = serializers.VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = models.User.objects.get(email=email)
                return Response({'msg': "user found in database"}, status=status.HTTP_200_OK)
            except models.User.DoesNotExist:
                return Response({'errors': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLogin(APIView):
    renderer_classes = [renderers.UserRenderers]
    def post(self, request, format=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successful...'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ["Invalid User",]}}, status=status.HTTP_404_NOT_FOUND)
            
class UserProfile(APIView):
    renderer_classes = [renderers.UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangePassword(APIView):
    renderer_classes = [renderers.UserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer =serializers.UserChangePassword(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Change Successfully...'}, status=status.HTTP_200_OK)
        
class SendPasswordReset(APIView):
    renderer_classes = [renderers.UserRenderers]
    def post(self, request, format=None):
        serializer = serializers.PasswordResentLink(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Link Sent...'}, status=status.HTTP_200_OK)
        
class UserPasswordReset(APIView):
    renderer_classes=[renderers.UserRenderers]
    def post(self, request, uid, token, format=None):
        serializer = serializers.UserPasswordReset(data=request.data, context={'uid': uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successfully...'}, status=status.HTTP_200_OK)