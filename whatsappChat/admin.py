from django.contrib import admin
from . import models

class indContact(admin.ModelAdmin):
    list_display = ['full_name', 'phone']

class conversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'sender', 'receiver']

class messageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'timestamp']

# Register your models here.
admin.site.register(models.phoneDetails, indContact)
admin.site.register(models.Conversation, conversationAdmin)
admin.site.register(models.Message, messageAdmin)