from django.urls import path
from .views import product_page, new_product_page

urlpatterns = [
    path('product/', product_page, name = "product_page"),
    path('new_product/', new_product_page, name = "new_product_page")
]