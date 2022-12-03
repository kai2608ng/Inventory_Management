from .models import Store
from product.models import Product
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

class SaleForm(forms.Form):
    product = forms.ChoiceField(
        required = True,
        widget = forms.Select(
            attrs = {
                "name": "product"
            }
        ),
        choices = [
            (product.id, product.product_name) 
            for product in Product.objects.all()
        ],
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
        }
    )

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 0:
            self.add_error("quantity", "Please enter a valid quantity")
        
        return quantity