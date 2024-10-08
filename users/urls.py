from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.form import CustomPasswordResetForm
from users.views import UserCreateView, email_verification, ProfileView, PasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('account-confirm/<str:token>/', email_verification, name='account-confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset')
]
