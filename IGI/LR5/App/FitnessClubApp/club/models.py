from django.db import models
from django.utils import timezone
from users.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class CommentsModel(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.username} ({self.rating})"

    @classmethod
    def get_average_rating(cls):
        return cls.objects.aggregate(models.Avg('rating'))['rating__avg'] or 0

class FAQModel(models.Model):
    quastion = models.TextField(unique=True, verbose_name='Вопрос', null=True)
    answer = models.TextField(verbose_name='Ответ', null=True)
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name='Дата сохранения', null=True)

    def __str__(self):
        return self.quastion[:50]+"..."
    class Meta:
        verbose_name = "Вопрос/Ответ"
        verbose_name_plural = "Вопросы/Ответы"

class VacancyModel(models.Model):
    name = models.TextField(unique=True, verbose_name='Наименование вакансии', null=True)
    description = models.TextField(verbose_name='Описание вакансии', null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class GymModel(models.Model):
    name = models.CharField('Название зала', max_length=100)
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото', upload_to='media/club/gym/img', blank=True, null=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class ScheduleModel(models.Model):
    name = models.CharField('Название занятия', max_length=100)
    gym = models.ForeignKey(GymModel, on_delete=models.CASCADE, verbose_name='Зал', related_name='schedules', )
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Тренер', related_name='instructed_schedules')
    users = models.ManyToManyField(User, blank=True, verbose_name='Участники занятия', related_name='participated_schedules', through='BookingModel')
    price = models.DecimalField(verbose_name='Стоимость занятия', max_digits=10, decimal_places=2, default=0.00)
    
    start_time = models.DateTimeField('Начало')
    end_time = models.DateTimeField('Окончание')
    
    
    max_participants = models.PositiveIntegerField('Макс. участников', default=10)
    @property
    def current_participants(self):
        return self.users.count()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Расписание'
        ordering = ['start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='end_time_after_start_time'
            )
        ]

    def __str__(self):
        return f"{self.name} в {self.gym.name} ({self.start_time})"

    def duration(self):
        """Длительность занятия в минутах"""
        return (self.end_time - self.start_time).total_seconds() / 60

    def is_available(self):
        """Есть ли свободные места"""
        return self.max_participants
    
    def get_participants(self):
        return self.max_participants - self.current_participants
    
class BookingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE, verbose_name='Занятие')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        unique_together = [['user', 'schedule']]

    def __str__(self):
        return f"{self.user.username} на {self.schedule}"
    