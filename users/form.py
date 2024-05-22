from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomPasswordResetForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label='Email', max_length=254, help_text='Введите ваш email')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ('email', 'country', 'phone', 'avatar')
