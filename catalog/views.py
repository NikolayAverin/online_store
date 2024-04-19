from django.shortcuts import render

from catalog.models import Product
from configurations import APPEALS
import json
import csv


def home_page(request):
    all_count = len(Product.objects.all())
    if all_count <= 5:
        context = {
            'title': 'skystore',
            'products': Product.objects.all()
        }
    else:
        context = {
            'title': 'skystore',
            'products': Product.objects.all()[(all_count - 5):]
        }
    print(context['products'])
    return render(request, 'catalog/home_page.html', context=context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data_to_write = {"name": name, "phone": phone, "message": message}
        print(f'{name} просит связаться по номеру {phone}. Его вопрос: {message}')
        with open(APPEALS, "a") as file:
            fc = csv.DictWriter(file, fieldnames=data_to_write.keys())
            fc.writerow(data_to_write)
    return render(request, 'catalog/contacts.html')
