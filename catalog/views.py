from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Contact, Category
from configurations import APPEALS
import csv


def home_page(request):
    products = Product.objects.all()
    context = {
        'title': 'Off-Road Market',
        'products': products
    }
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
    elif request.method == 'GET':
        context = {
            'title': 'Контакты',
            'contacts': Contact.objects.last()
        }
    return render(request, 'catalog/contacts.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': 'Товар',
        'products': product
    }
    return render(request, 'catalog/product_detail.html', context)


def add_product(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'catalog/add_product.html', context)
    elif request.method == 'POST':
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        price = request.POST.get('product_price')
        photo = request.POST.get('product_photo')
        category_id = request.POST.get('product_id')
        category = Category.objects.get(id=category_id)
        Product.objects.create(name=name, description=description, price=price, photo=photo, category=category)
        return render(request, 'catalog/add_product.html', context)
