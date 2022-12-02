from django.urls import path
from .views import (
    product_page, new_product_page, 
    edit_product_page, delete_product_page)

urlpatterns = [
    path('product/', product_page, name = "product_page"),
    path('new_product/', new_product_page, name = "new_product_page"),
    path("edit_product/<int:product_id>/", edit_product_page, name = "edit_product_page"),
    path("delete_product/<int:product_id>/", delete_product_page, name = "delete_product_page")
]