from django.urls import path
from .views import home_page, new_store_page, store_detail_page

urlpatterns = [
    path('home/', home_page, name = "home_page"),
    path('new_store/', new_store_page, name = "new_store_page"),
    path('<str:store_name>/', store_detail_page, name = "store_detail_page")
]