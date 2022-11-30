from django import forms
from product.models import Product

class ProductForm(forms.models.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'store']
        widget = {
            "product_name": forms.TextInput(
                attrs = {
                    "id": "product-name",
                    "name": "product_name"
                }
            ),
            "store": forms.HiddenInput(
                attrs = {
                    'id': "store",
                    'name': 'store',
                }
            )
        }
        error_messages = {
            "product_name": {"required": "Please enter a valid Product name"}
        }
    