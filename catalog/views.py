from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product, Contact
from configurations import APPEALS
import csv


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactsListView(ListView):
    model = Contact

    def get_queryset(self):
        qs = super().get_queryset()
        max_pk = 0
        for item in qs:
            if item.pk > max_pk:
                max_pk = item.pk
        qs = qs.filter(pk=max_pk)
        return qs

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data_to_write = {"name": name, "phone": phone, "message": message}
        print(f'{name} просит связаться по номеру {phone}. Его вопрос: {message}')
        with open(APPEALS, "a") as file:
            fc = csv.DictWriter(file, fieldnames=data_to_write.keys())
            fc.writerow(data_to_write)
        return redirect(reverse_lazy('catalog:home_page'))


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "description", "price", "photo", "category")
    success_url = reverse_lazy('catalog:home_page')
