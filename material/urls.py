from django.urls import path
from .views import material_page, new_material_page

urlpatterns = [
    path('material/', material_page, name = "material_page"),
    path('new_material/', new_material_page, name = "new_material_page")
]