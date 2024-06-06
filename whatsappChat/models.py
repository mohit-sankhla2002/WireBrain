from django.db import models

# Create your models here.
class phoneDetails(models.Model):
    full_name = models.CharField(max_length=120, blank=False)
    email = models.EmailField(max_length=80)
    phone = models.CharField(max_length=10, unique=True, blank=False)