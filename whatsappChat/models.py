from django.db import models
from authApp import models as authModels
from django.utils import timezone

# Create your models here.
class phoneDetails(models.Model):
    full_name = models.CharField(max_length=120, blank=False)
    email = models.EmailField(max_length=80)
    phone = models.CharField(max_length=15, unique=True, blank=False)

# class WhatsAppAccount(models.Model):
#     phone_number = models.CharField(max_length=20, unique=True)
#     display_name = models.CharField(max_length=100)
#     wa_id = models.CharField(max_length=20, unique=True)

class Conversation(models.Model):
    conversation_id = models.CharField(max_length=100, unique=True)
    phone_id = models.CharField(max_length=100, null=True, blank=True)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    expiration_timestamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.conversation_id

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    message_id = models.CharField(max_length=100, unique=True)
    message_type = models.CharField(max_length=20)
    content = models.TextField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)