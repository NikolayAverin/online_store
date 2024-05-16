from django.db import models


class Blog(models.Model):
    """Модель блога"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blog', verbose_name='Изображение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    email = models.EmailField(verbose_name='Почта', null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
