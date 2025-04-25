from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_notifications_notification_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='notification_type',
            field=models.CharField(
                default='self',
                max_length=30,
                choices=[
                    ('self', 'Self'),
                    ('group_request', 'Group Request'),
                    ('assignment', 'Assignment'),
                    ('result', 'Result')
                ],
            ),
        ),
    ]
