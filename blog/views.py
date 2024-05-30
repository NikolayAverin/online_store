from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogForm, BlogModeratorForm
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """Создание слага"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        """Вывод только опубликованных записей"""
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """Увеличение количества просмотров записи"""
        """Отправка письма при просмотре записи 100 раз"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail('Поздравляем, ваша запись просмотрена 100 раз!',
                      f'Запись {self.object.title} просмотрена 100 раз!',
                      settings.EMAIL_HOST_USER, [self.object.email])
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published', 'email']
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """Создание слага"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на просмотр записи"""
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Выбор формы для редактирования блога"""
        user = self.request.user
        if user.has_perm('blog.can_deactivate'):
            return BlogModeratorForm
        raise PermissionDenied


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
