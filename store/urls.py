from django.urls import path
from .views import home_page, new_store_page

urlpatterns = [
    path('home/', home_page, name = "home_page"),
    path('new_store/', new_store_page, name = "new_store_page"),
]