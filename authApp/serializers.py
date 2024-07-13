from rest_framework import serializers
from . import models
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import utils

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'profile_photo','email', 'username', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password not matches...")
        return attrs
    
    def create(self, validated_data):
        otp = utils.generate_otp()
        user = models.User.objects.create_user(**validated_data)
        user.otp = otp
        user.is_verified = False
        user.save()
        
        data = {
            'subject': 'Your OTP Code',
            'body': f'Your OTP code is {otp}',
            'to_email': user.email
        }
        utils.Util.send_mail(data)

        return user
    
class AdminRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone', 'password', 'password2', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password not matches...")
        return attrs

    def create(self, validate_data):
        return models.User.objects.create_superuser(**validate_data, )
        
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = models.User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'username', "email", 'phone']

class UserChangePassword(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = models.User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password not matches...")
        user.set_password(password)
        user.save()
        return attrs
    
class PasswordResentLink(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email=email)
            uid = str(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/reset/"+uid+"/"+token
            print(link)
            data = {
                'subject': "Reset your password",
                "body": "Click the link to reset your password "+link,
                'to_email': user.email
            }
            utils.Util.send_mail(
                data=data
            )
            return attrs
        else:
            raise serializers.ValidationError("You are not registered User...")
        
class UserPasswordReset(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = models.User
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password not matches...")
            user = models.User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or Expired...")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user=user, token=token)
            raise serializers.ValidationError("Token is not valid or Expired...")