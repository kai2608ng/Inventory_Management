from .models import Store
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