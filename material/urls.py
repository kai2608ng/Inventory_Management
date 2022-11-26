from django.urls import path
from .views import material_page

urlpatterns = [
    path('', material_page, name = "material_page")
]