# Generated by Django 5.0.4 on 2024-07-13 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createTeam', '0008_alter_team_apitoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='apiToken',
            field=models.CharField(max_length=1000),
        ),
    ]