from django.urls import path
from .views import home_page

urlpatterns = [
    path('home/<str:username>/', home_page, name = "home_page")
]