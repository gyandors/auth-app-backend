# Generated by Django 5.1.4 on 2024-12-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_user_otp_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_2fa_enabled',
            field=models.BooleanField(default=False),
        ),
    ]