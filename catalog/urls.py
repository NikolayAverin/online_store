from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home_page, contacts, product_detail, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', product_detail, name='product_detail'),
    path('add_product', add_product, name='add_product')
]
