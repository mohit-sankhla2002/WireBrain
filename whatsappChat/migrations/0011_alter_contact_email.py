# Generated by Django 5.0.4 on 2024-06-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappChat', '0010_contact_remove_message_conversation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=80, null=True, unique=True),
        ),
    ]
