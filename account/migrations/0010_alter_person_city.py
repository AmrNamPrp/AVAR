# Generated by Django 5.1.7 on 2025-04-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_person_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='city',
            field=models.CharField(choices=[('خارج سوريا', 'خارج سوريا'), ('ادلب', 'ادلب'), ('دمشق', 'دمشق'), ('حلب', 'حلب'), ('ريف دمشق', 'ريف دمشق'), ('حماه', 'حماه'), ('حمص', 'حمص'), ('درعا', 'درعا'), ('القنيطرة', 'القنيطرة'), ('السويداء', 'السويداء'), ('دير الزور', 'دير الزور'), ('رقه', 'رقه'), ('الحسكة', 'الحسكة'), ('اللاذقية', 'اللاذقية'), ('طرطوس', 'طرطوس')], max_length=30, null=True),
        ),
    ]
