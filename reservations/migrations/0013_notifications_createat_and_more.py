# Generated by Django 5.1.7 on 2025-04-24 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0012_remove_notifications_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='notifications_reservation',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
