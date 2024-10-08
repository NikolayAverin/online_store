from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Contact, Version, Category
from catalog.services import get_category_from_cache, get_products_from_cache
from configurations import APPEALS
import csv


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        """Возвращение последней активной версии товара в списке товаров"""
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        for product in products:
            versions = Version.objects.filter(product=product)
            active_version = versions.filter(activity=True)
            if active_version:
                product.name_version = active_version.last().name
                product.number_version = active_version.last().version
        context['object_list'] = products
        return context

    def get_queryset(self):
        """Возвращение товаров из кэша"""
        return get_products_from_cache()


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('catalog:home_page')


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home_page')

    def form_valid(self, form):
        """Указываем почту продавца"""
        product = form.save()
        user = self.request.user
        product.seller = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home_page')

    def get_context_data(self, **kwargs):
        """Добавление версий товара при редактировании товара"""
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Добавление версий товара при редактировании товара"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        """Выбор формы для редактирования товара"""
        user = self.request.user
        if user == self.object.seller:
            return ProductForm
        if user.has_perm('catalog.can_deactivate') and user.has_perm('catalog.can_edit_description') and user.has_perm('catalog.can_edit_category'):
            return ProductModeratorForm
        raise PermissionDenied


class ContactsListView(ListView):
    model = Contact

    def get_queryset(self):
        """Выбор последней записи из таблицы контактов"""
        qs = super().get_queryset()
        max_pk = 0
        for item in qs:
            if item.pk > max_pk:
                max_pk = item.pk
        qs = qs.filter(pk=max_pk)
        return qs

    def post(self, request, *args, **kwargs):
        """Запись заявки в csv файл и перенаправление на главную страницу"""
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data_to_write = {"name": name, "phone": phone, "message": message}
        print(f'{name} просит связаться по номеру {phone}. Его вопрос: {message}')
        with open(APPEALS, "a") as file:
            fc = csv.DictWriter(file, fieldnames=data_to_write.keys())
            fc.writerow(data_to_write)
        return redirect(reverse_lazy('catalog:home_page'))


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        """Возвращение категорий из кэша"""
        return get_category_from_cache()
