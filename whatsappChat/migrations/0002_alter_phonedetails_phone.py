# Generated by Django 5.0.4 on 2024-06-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappChat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonedetails',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]