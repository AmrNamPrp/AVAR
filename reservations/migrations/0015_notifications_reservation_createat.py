# Generated by Django 5.1.7 on 2025-04-24 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0014_remove_notifications_createat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications_reservation',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
