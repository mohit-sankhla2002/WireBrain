# Generated by Django 5.0.4 on 2024-07-13 12:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createTeam', '0006_alter_team_apitoken_alter_team_team_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_leader',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]