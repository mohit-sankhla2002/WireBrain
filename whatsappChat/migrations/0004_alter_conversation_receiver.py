# Generated by Django 5.0.4 on 2024-06-24 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappChat', '0003_conversation_whatsappaccount_message_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_conversations', to=settings.AUTH_USER_MODEL),
        ),
    ]