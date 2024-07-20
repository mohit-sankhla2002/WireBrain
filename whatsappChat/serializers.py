from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from .utils import get_whatsapp_credentials
from . import models
import openpyxl
import requests

class credentialSerializer(serializers.Serializer):
    def get_credentials(self):
        user = self.context.get('user')
        teamId = user.team.id
        try:
            return get_whatsapp_credentials(teamId)
        except KeyError:
            raise ValidationError("Invalid Access Token....")


class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ['full_name','email','phone']

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User context is required")
        return models.Contact.objects.create(user=user, **validated_data)
    

class getTemplatesSerializer(serializers.Serializer):
    wbId = serializers.CharField()
    authToken = serializers.CharField()

    def get_message_templates(self):
        user = self.context.get('user')
        teamId = user.team.id
        credentials = get_whatsapp_credentials(teamId)
        wbId = credentials['whatsapp_business_id']
        authToken = credentials['auth_token']
        url = f"https://graph.facebook.com/v20.0/{wbId}/message_templates?category=utility"
        headers = {
        'Authorization': f'Bearer {authToken}'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValidationError(str(e))


class excelSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, file):
        if not file.name.endswith('.xlsx'):
            raise serializers.ValidationError('This is not required file')
        return file

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        wb = openpyxl.load_workbook(csv_file)
        sheet = wb.active
        user_data_list = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            full_name, email, mobile_number = row
            if full_name and email and mobile_number:
                user_data_list.append(models.phoneDetails(full_name=full_name, email=email, phone=mobile_number))
        
        try:
            models.phoneDetails.objects.bulk_create(user_data_list)
        except IntegrityError as e:
            raise serializers.ValidationError({'mobile_number':"Duplicate Mobile Number Found"}) 
        return user_data_list
    

from rest_framework import serializers

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

class MessageSerializer(PhoneSerializer):
    message = serializers.CharField()

class MediaSerializer(PhoneSerializer):
    media = serializers.FileField()

    def validate_media(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Media file size must be less than or equal to 5 MB.")
        return value
    

