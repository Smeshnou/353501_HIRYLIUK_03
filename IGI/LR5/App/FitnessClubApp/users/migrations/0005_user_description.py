# Generated by Django 5.2.1 on 2025-06-01 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(max_length=200, null=True, verbose_name='Род деятельности'),
        ),
    ]
