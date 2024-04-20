from django.urls import path

from catalog.views import home_page, contacts

urlpatterns = [
    path('', home_page),
    path('contacts/', contacts)
]
