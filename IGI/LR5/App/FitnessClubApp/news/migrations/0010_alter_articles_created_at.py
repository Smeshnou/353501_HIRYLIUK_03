# Generated by Django 5.2.1 on 2025-06-03 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_articles_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 6, 22, 24, 285640, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата сохранения'),
        ),
    ]
