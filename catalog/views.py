from django.shortcuts import render
from configurations import APPEALS
import json


def home_page(request):
    return render(request, 'catalog/home_page.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data_to_write = {"name": name, "phone": phone, "message": message}
        print(f'{name} просит связаться по номеру {phone}. Его вопрос: {message}')
        with open(APPEALS, "a") as file:
            json.dump(data_to_write, file, indent=4)
    return render(request, 'catalog/contacts.html')
