from django import forms
from django.forms import BooleanField

from blog.models import Blog


class StyleFormMixin:
    """Стилизация формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'email')


class BlogModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('is_published',)
