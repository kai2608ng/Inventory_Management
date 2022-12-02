from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from .forms import ProductForm
from .models import Product
from store.models import Store
from material.models import Material, MaterialQuantity
from material.forms import MaterialQuantityForm

def stupid_authentication(request):
    token = request.session.get('token', None)
    return authenticate(request, token = token)

def product_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        products = Store.objects.get(user = valid_token_user).product_entries.all()
        return render(request, "product/product.html", {"username": username, 'products': products})

    return redirect(reverse('login_page'))

def new_product_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        product_form = ProductForm()
        material_quantity_forms = [MaterialQuantityForm()]

        if request.method == "POST":
            product_name = request.POST['product_name']
            materials = request.POST.getlist("material")
            quantities = request.POST.getlist("quantity")
                
            material_quantity_forms = []
            material_quantity_error_flag = False

            store = Store.objects.get(user = valid_token_user)

            product_form = ProductForm(data = {
                'product_name': product_name, 
                'store': store
            })
            
            # validate all the material quantity forms
            for material_id, quantity in zip(materials, quantities):
                material_quantity_form = MaterialQuantityForm(data = {
                    "material": material_id,
                    "quantity": quantity
                })

                material_quantity_forms.append(material_quantity_form)

                if not material_quantity_form.is_valid():
                    material_quantity_error_flag = True

            # Show error for the specific material quantity form 
            if material_quantity_error_flag:
                return render(
                    request, 
                    "product/new_product.html", 
                    {
                        "username": username, 
                        'product_form': product_form,
                        "material_quantity_forms": material_quantity_forms
                    }
                )

            if product_form.is_valid() and not material_quantity_error_flag:
                product = product_form.save()

                for material_id, quantity in zip(materials, quantities):
                    material = Material.objects.get(pk = material_id)
                    try:
                        MaterialQuantity.objects.create(
                            product = product,
                            material = material,
                            quantity = quantity
                        )
                    except IntegrityError:
                        continue;

                # Remove all the data 
                material_quantity_forms = [MaterialQuantityForm()]
                product_form = ProductForm()
                return render(
                    request, 
                    "product/new_product.html", 
                    {
                        "username": username, 
                        'product_form': product_form,
                        "material_quantity_forms": material_quantity_forms
                    }
                )
            
        return render(
            request, 
            "product/new_product.html", 
            {
                "username": username, 
                'product_form': product_form,
                "material_quantity_forms": material_quantity_forms
            }
        )

    return redirect(reverse('login_page'))

def edit_product_page(request, username, product_id):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        product = Product.objects.get(pk = product_id)
        material_quantities = MaterialQuantity.objects.filter(product__id = product_id)
        store = Store.objects.get(user = valid_token_user)
        product_initial_data = {
            "product_name": product.product_name,
            "store": store
        }
        mq_initial_data = {
            "material": material_quantities[0].material.material_name,
            "quantity": material_quantities[0].quantity
        }
        product_form = ProductForm(initial = product_initial_data)
        material_quantity_form = MaterialQuantityForm(initial = mq_initial_data)

        if request.method == "POST":
            product_name = request.POST["product_name"]
            data = {
                "product_name": product_name,
                "store": store
            }
            product_form = ProductForm(data = data, instance = product)
            if product_form.is_valid():
                product_form.save()

        return render(
            request, "product/edit_product.html", 
            {
                'username': username, 
                'product_id': product_id, 
                "product_form": product_form,
                "material_quantity_form": material_quantity_form
            })

def delete_product_page(request, username, product_id):
    try:
        product = Product.objects.get(pk = product_id)
        product.delete()
    except Product.DoesNotExist:
        return render(request, "product/product_error.html", {"username": username})
    return redirect(reverse("product_page", args = (username, )))