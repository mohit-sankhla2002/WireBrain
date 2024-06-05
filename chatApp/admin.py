from django.contrib import admin
from . import models

class messageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'conversation']

# Register your models here.
admin.site.register(models.messages, messageAdmin)
admin.site.register(models.conversation)