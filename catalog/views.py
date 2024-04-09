from django.shortcuts import render


def home_page(request):
    return render(request, 'catalog/home_page.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')
