from rest_framework import serializers
from django.db import IntegrityError
from . import models
import openpyxl

class indPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.phoneDetails
        fields = ['full_name', 'phone']

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