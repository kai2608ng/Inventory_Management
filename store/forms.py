from .models import Store
from product.models import Product
from material.models import MaterialQuantity, Material
from django import forms

class StoreForm(forms.models.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'user']
        widgets = {
            "store_name": forms.TextInput(
                attrs = {
                    "id": "store-name",
                    "name": "store_name",
                }
            )
        }
        error_messages = {
            "store_name": {"required": "Please enter a store name"}
        }

class SalesForm(forms.Form):
    def __init__(self, track_current_quantity, choices, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        self.track_current_quantity = track_current_quantity
        self.fields['product'] = forms.ChoiceField(
            required = True,
            widget = forms.Select(
                attrs = {
                    "name": "product"
                }
            ),
            choices = choices,
            error_messages = {
                "required": "Please select a product"
            }
        )
    
    quantity = forms.IntegerField(
        required = True,
        widget = forms.NumberInput(
            attrs = {
                "name": "quantity"
            }
        ),
        error_messages = {
            "required": "Please enter a valid quantity"
        },
        initial = 0
    )   

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 0:
            self.add_error("quantity", "Please enter a valid quantity")
        
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data["product"]
        product_quantity = cleaned_data["quantity"]

        material_quantities = MaterialQuantity.objects.filter(product__id = product_id)
        for material_quantity in material_quantities:
            if material_quantity.material.pk not in self.track_current_quantity:
                material_current_quantity = Material.objects.get(pk = material_quantity.material.pk).current_capacity
                self.track_current_quantity.update({material_quantity.material.pk: material_current_quantity})

            temp_current_quantity = self.track_current_quantity[material_quantity.material.pk] - product_quantity * material_quantity.quantity

            if temp_current_quantity < 0:
                self.add_error(None, "Insufficient Material")
                break

            self.track_current_quantity[material_quantity.material.pk] = temp_current_quantity

        return cleaned_data