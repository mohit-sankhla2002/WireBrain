# Generated by Django 5.0.4 on 2024-07-13 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createTeam', '0009_alter_team_apitoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='apiToken',
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_leader',
        ),
    ]