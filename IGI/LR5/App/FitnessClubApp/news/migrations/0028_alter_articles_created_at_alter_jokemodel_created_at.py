# Generated by Django 5.2.1 on 2025-06-03 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0027_articles_img_alter_articles_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 22, 36, 34, 523591, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата сохранения'),
        ),
        migrations.AlterField(
            model_name='jokemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 22, 36, 34, 534591, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата сохранения'),
        ),
    ]
