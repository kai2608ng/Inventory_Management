from django.urls import path
from .views import product_page

urlpatterns = [
    path('', product_page, name = "product_page")
]