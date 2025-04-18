# Generated by Django 5.1.7 on 2025-03-19 13:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_alter_review_real_estate_delete_comments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='real_estate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='reservations.realestate'),
        ),
        migrations.CreateModel(
            name='NewRealEstate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, choices=[('خارج سوريا', 'خارج سوريا'), ('ادلب', 'ادلب'), ('دمشق', 'دمشق'), ('حلب', 'حلب'), ('ريف دمشق', 'ريف دمشق'), ('حماه', 'حماه'), ('حمص', 'حمص'), ('درعا', 'درعا'), ('القنيطرة', 'القنيطرة'), ('السويداء', 'السويداء'), ('دير الزور', 'دير الزور'), ('القامشلي', 'القامشلي'), ('الحسكة', 'الحسكة'), ('اللاذقية', 'اللاذقية'), ('طرطوس', 'طرطوس')], max_length=30, null=True, verbose_name='المحافظة')),
                ('town', models.CharField(blank=True, max_length=30, null=True, verbose_name='المدينة او البلدة')),
                ('type', models.CharField(blank=True, choices=[('مزرعة', 'مزرعة'), ('فيلا', 'فيلا'), ('شقة', 'شقة')], max_length=30, null=True, verbose_name='نوع العقار')),
                ('notes', models.CharField(blank=True, max_length=500, null=True, verbose_name='ملاحظات')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
