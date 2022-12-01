from django import forms
from .models import Material
from django.core.exceptions import ValidationError

class MaterialForm(forms.models.ModelForm):
    class Meta:
        model = Material
        fields = ['material_name', 'price', 'max_capacity', 'current_capacity', 'store']
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
            ),
        }
        error_messages = {
            "material_name": {"required": "Please key in a valid material name"},
            "price": {"required": "Please key in a valid price"},
            "max_capacity": {"required": "Please enter a valid max capacity"},
            "current_capacity": {"required": "Please enter a valid current capacity"}
        }    

    def clean(self):
        cleaned_data = super().clean()
        max_capacity = cleaned_data.get("max_capacity")
        current_capacity = cleaned_data.get("current_capacity")

        if current_capacity and max_capacity and current_capacity > max_capacity:
            self.add_error("current_capacity", "Your current capacity is larger than max capacity!")
            self.add_error("max_capacity", "Your current capacity is larger than max capacity!")

        return cleaned_data