from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Articles(models.Model):
    TYPE_CHOICES = [
        ('general', 'Общие'),
        ('programming', 'Программирование'),
        ('knock-knock', 'Тук-тук'),
    ]
    
    api_id = models.IntegerField(default=1, unique=True, verbose_name='ID из API')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип шутки', null=True)
    setup = models.TextField(verbose_name='Вопрос/Утверждение', null=True)
    punchline = models.TextField(verbose_name='Ответ/Панчлайн', null=True)
    created_at = models.DateTimeField(default=timezone.now(), verbose_name='Дата сохранения', null=True)
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.setup[:50]}..."