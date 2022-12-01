from django.urls import path
from .views import (
    material_page, new_material_page, 
    edit_material_page, delete_material_page)

urlpatterns = [
    path('material/', material_page, name = "material_page"),
    path('new_material/', new_material_page, name = "new_material_page"),
    path('edit_material/<int:material_id>/', edit_material_page, name = "edit_material_page"),
    path('delete_material/<int:material_id>/', delete_material_page, name = "delete_material_page")
]