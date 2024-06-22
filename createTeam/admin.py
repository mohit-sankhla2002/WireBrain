from django.contrib import admin
from . import models

# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_name', 'team_type']
    list_filter = ['team_type']

# Now register the new UserAdmin...

admin.site.register(models.Team, TeamAdmin)