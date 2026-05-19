
from django.db import models
from accounts.models import User

#Выборы для фильтров
COURSE_TYPES = [
    ('qualification', 'Повышение квалификации'),
    ('retraining', 'Переподготовка'),
    ('labor_protection', 'Охрана труда'),
]

STATUS_CHOICES = [
    ('new', 'Новая'),
    ('in_progress', 'Идёт обучение'),
    ('completed', 'Обучение завершено'),
]

PAYMENT_METHODS = [
    ('card', 'Банковская карта'),
    ('cash', 'Наличные'),
    ('invoice', 'По счёту (для организаций)'),
]

#Модель заявки
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Пользователь')
    course_type = models.CharField('Тип курса', max_length=20, choices=COURSE_TYPES)
    date = models.DateField('Дата начала')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата подачи', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} {self.user.login} — {self.get_course_type_display()}'

    def get_status_badge(self):
        return {
            'new': 'warning',
            'in_progress': 'primary',
            'completed': 'success',
        }.get(self.status, 'secondary')

    def can_advance(self):
        return self.status != 'completed'

#Модель отзыв
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    application = models.OneToOneField(
        Application, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='review',
        verbose_name='Заявка',
    )
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Оценка', default=5, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.user.login} (оценка {self.rating})'
