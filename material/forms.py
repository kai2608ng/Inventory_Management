from django import forms
from .models import Material

class MaterialForm(forms.models.ModelForm):
    class Meta:
        model = Material
        fields = ['material_name', 'price', 'max_capacity', 'current_capacity']
        widgets = {
            'material_name': forms.TextInput(
                attrs = {
                    'id': "material-name",
                    'name': 'material_name'
                }
            ),
            'price': forms.TextInput(
                attrs = {
                    'id': 'price',
                    'name': 'price'
                }
            ),
             "max_capacity": forms.NumberInput(
                attrs = {
                    "id": "max-capacity",
                    "name": "max_capacity"
                }
            ),
            "current_capacity": forms.NumberInput(
                attrs = {
                    "id": "current-capacity",
                    "name": "current_capacity"
                }
            )
        }
        errors_message = {
            "material_name": {"required": "Please key in a valid material name"},
            "price": {"required": "Please key in a valid price"},
            "max_capacity": {"required": "Please enter a valid max capacity"},
            "current_capacity": {"required": "Please enter a valid current capacity"}
        }
           