from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Product, Category
from configurations import *
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open(CATALOG) as file:
            result = json.load(file)
        result_list = []
        for i in result:
            if i['model'] == 'catalog.category':
                result_list.append(i['fields'])
        return result_list

    @staticmethod
    def json_read_products():
        with open(CATALOG) as file:
            result = json.load(file)
        result_list = []
        for i in result:
            if i['model'] == 'catalog.product':
                result_list.append(i['fields'])
        return result_list

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        Category.objects.all().delete()
        Product.objects.all().delete()

        category_for_create = []
        product_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(Category(**category))

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(Product(name=product["name"],
                            description=product["description"],
                            category=Category.objects.get(pk=product["category"]),
                            price=product["price"]))

        Product.objects.bulk_create(product_for_create)
