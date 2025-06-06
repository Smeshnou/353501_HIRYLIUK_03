# Generated by Django 5.2.1 on 2025-06-03 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_alter_commentsmodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulemodel',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Стоимость занятия'),
        ),
        migrations.AlterField(
            model_name='commentsmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 9, 14, 29, 545659, tzinfo=datetime.timezone.utc)),
        ),
    ]
