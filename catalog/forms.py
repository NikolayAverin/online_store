from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    """Стилизация формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'seller', 'is_active')

    def clean_name(self):
        """Валидация названия продукта"""
        cleaned_name = self.cleaned_data['name']
        if cleaned_name.lower() in FORBIDDEN_WORDS:
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return cleaned_name

    def clean_description(self):
        """Валидация описания продукта"""
        cleaned_description = self.cleaned_data['description']
        if cleaned_description.lower() in FORBIDDEN_WORDS:
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return cleaned_description


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_active')


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
