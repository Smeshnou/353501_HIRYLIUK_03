from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Clients', 'Клиент'),
        ('Instructors', 'Инструктор'),
        ('Admins', 'Администратор'),
    )
    role = models.CharField(choices=ROLE_CHOICES, default='client', verbose_name='Роль')
    description = models.CharField(max_length=200, null=True, verbose_name='Род деятельности')
    photo = models.FileField(upload_to="users/img/", blank=True, verbose_name="Фотография")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    phone_number = PhoneNumberField(region='BY', blank=True, null=True, verbose_name="Телефон (Беларусь)")
