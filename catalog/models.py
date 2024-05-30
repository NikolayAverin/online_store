from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """Категория товара"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Товар"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='catalog', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, **NULLABLE)
    updated_at = models.DateField(verbose_name='Дата последнего изменения', auto_now=True, **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', **NULLABLE)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='seller', **NULLABLE)
    is_active = models.BooleanField(verbose_name='Прошел ли проверку', default=False)

    def __str__(self):
        return f'{self.name} - {self.price} руб'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            ('can_deactivate', 'deactivate product'),
            ('can_edit_description', 'edit description product'),
            ('can_edit_category', 'edit category product'),
        ]


class Version(models.Model):
    """Версия товара"""
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    version = models.IntegerField(verbose_name='Версия')
    name = models.CharField(max_length=100, verbose_name='Название версии')
    activity = models.BooleanField(verbose_name='Активность версии', default=True)

    def __str__(self):
        return f'{self.product} - {self.version}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class Contact(models.Model):
    """Контакты"""
    country = models.CharField(max_length=50, verbose_name='Страна')
    inn = models.IntegerField(verbose_name='ИНН')
    address = models.CharField(max_length=100, verbose_name='Адрес')

    def __str__(self):
        return f'{self.country}, {self.inn}, {self.address}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
