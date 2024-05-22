import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, FormView

from config.settings import EMAIL_HOST_USER
from users.form import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка письма с токеном для верификации аккаунта"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/account-confirm/{token}/'
        send_mail(
            subject='Подтверждение аккаунта',
            message=f'Перейдите по ссылке для подтверждения аккаунта {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка письма с новым паролем"""
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()
        send_mail(
            subject='Смена пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Получение текущего пользователя"""
        return self.request.user


def email_verification(request, token):
    """Проверка токена и активация пользователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
