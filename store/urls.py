from django.urls import path
from .views import home_page, new_store_page, restock_page, sales_page

urlpatterns = [
    path('home/', home_page, name = "home_page"),
    path('new_store/', new_store_page, name = "new_store_page"),
    path('restock/', restock_page, name = "restock_page"),
    path('sales/', sales_page, name = "sales_page"),
]