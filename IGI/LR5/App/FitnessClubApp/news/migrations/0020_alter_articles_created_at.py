# Generated by Django 5.2.1 on 2025-06-03 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_alter_articles_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 8, 50, 40, 116581, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата сохранения'),
        ),
    ]
