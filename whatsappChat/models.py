from django.db import models
from authApp import models as authModels
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(authModels.User, related_name='user', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120, blank=False)
    email = models.EmailField(max_length=80, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=False)

    def __str__(self):
        return self.full_name

chats = settings.MONGO_DB['chats']