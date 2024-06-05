from rest_framework import serializers
from authApp import models as authAppmodel
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AddMemberSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        logged_user = self.context.get('user')
        if logged_user.is_admin == False:
            raise serializers.ValidationError("You are not authorized to add members...")
        if authAppmodel.User.objects.filter(email=email).exists():
            send_user = authAppmodel.User.objects.get(email=email)
            if send_user.is_admin == True:
                raise serializers.ValidationError("Not authorized to admin user...")
            uid = urlsafe_base64_encode(force_bytes(logged_user.id))
            token = PasswordResetTokenGenerator().make_token(send_user)
            link = "http://localhost:3000/addMember/"+uid+"/"+token
            print(link)
            # print(logged_user.team.id)
            return attrs
        else:
            raise serializers.ValidationError("Email not found...")
        
class AcceptInvitationSerializer(serializers.Serializer):
    def validate(self, attrs):
        uid = self.context.get('uid')
        token = self.context.get('token')
        user = self.context.get('user')
        id = smart_str(urlsafe_base64_decode(uid))
        if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or Expired...")
        print(user.team)
        admin_user = authAppmodel.User.objects.get(id=id)
        user.team = admin_user.team
        user.save()
        print(user.team)
        return super().validate(attrs)
    
class ChatUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = authAppmodel.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_admin' ]