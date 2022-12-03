from django import forms
from .models import Material, MaterialQuantity

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

class MaterialQuantityForm(forms.Form):
    def __init__(self, track_material, choices, *args, **kwargs):
        super(MaterialQuantityForm, self).__init__(*args, **kwargs)
        self.track_material = track_material
        self.fields["material"] = forms.ChoiceField(
        required = True, 
        widget = forms.Select(
            attrs = {
                "name": "material"
            }),
        choices = choices
    )

    quantity = forms.fields.IntegerField(
        required = True,
        widget = forms.NumberInput(
            attrs = {
                "name": "quantity"
            }
        ),
        initial = 0,
        error_messages = {
            "required": "Please key in a valid quantity"
        }
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            self.add_error("quantity", "Please enter a valid quantity")

        return quantity

    def clean_material(self):
        material = self.cleaned_data["material"]
        if not material:
            self.add_error("material", "Please select a material")

        if material in self.track_material:
            self.add_error(None, "Material Duplicated")
        else:
            self.track_material.append(material)
        

        return material
