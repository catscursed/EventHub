from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Event(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Название мероприятия'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    logo = models.ImageField(
        upload_to='media/event_logos',
        verbose_name='Логотип'
    )
    event_date = models.DateTimeField(
        verbose_name='Дата проведения'
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания объекта'
    )
    location = models.CharField(
        max_length=123,
        verbose_name='Место проведения'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена билета'
    )
    available = models.PositiveSmallIntegerField(
        verbose_name='Количество доступных билетов'
    )
    duration = models.CharField(
        max_length=50,
        verbose_name='Продолжительность'
    )
    is_active = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Активен'),
            (2, 'Не активен')
        ),
        default=1,
        verbose_name='Статус активности'
    )
    is_main = models.PositiveSmallIntegerField(
        choices=(
            (1, 'На главную'),
            (2, 'В каталог')
        ),
        default=2,
        verbose_name='Вывод ивента на главную'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  # генерируется slug только если он пустой
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='Мероприятие'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Кол-во билетов'
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата покупки'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Итоговая цена'
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'В обработке'),
            (2, 'Оплачен'),
            (3, 'Произошла ошибка при оплате')
        ),
        default=1,
        verbose_name='Статус оплаты'
    )
    ticket_code = models.CharField(
        max_length=36
    )

    def __str__(self):
        return f"Клиент -> {self.user} Заказал -> {self.event}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
