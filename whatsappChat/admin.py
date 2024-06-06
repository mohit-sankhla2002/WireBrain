from django.contrib import admin
from . import models

class indContact(admin.ModelAdmin):
    list_display = ['full_name', 'phone']

# Register your models here.
admin.site.register(models.phoneDetails, indContact)