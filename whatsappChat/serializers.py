from rest_framework import serializers
from . import models

class indPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.phoneDetails
        fields = ['full_name', 'phone']
