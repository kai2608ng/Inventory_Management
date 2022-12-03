from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.db.models import F
from .models import Store
from .forms import StoreForm, SalesForm
from product.models import Product
from material.models import Material

User = get_user_model()

def stupid_authentication(request):
    token = request.session.get('token', None)
    return authenticate(request, token = token)

def home_page(request, username):
    valid_token_user = stupid_authentication(request)
    
    if valid_token_user:
        auth_login(request, valid_token_user)
        stores = Store.objects.filter(user = valid_token_user)
        return render(request, "store/home.html", {'username': username, 'stores': stores})

    return redirect(reverse("login_page"))

def new_store_page(request, username):
    valid_token_user = stupid_authentication(request)
    if valid_token_user:
        form = StoreForm()

        if request.method == "POST":
            store_name = request.POST["store_name"]
            form = StoreForm(data = {"store_name": store_name, "user": valid_token_user})

            if form.is_valid():
                form.save()
                return redirect(reverse('home_page', args = (username, )))

        return render(request, "store/new_store.html", {"username": username, "form": form})
    
    return redirect(reverse("login_page"))
    
def restock_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        if request.method == "POST":
            materials = request.POST.getlist("material")
            restock_capacities = request.POST.getlist("restock_capacity")
            for material_id, restock in zip(materials, restock_capacities):
                current_capacity = Material.objects.get(pk = int(material_id)).current_capacity
                Material.objects.update_or_create(pk = material_id, defaults = {'current_capacity': current_capacity + int(restock)})

            return render(request, "store/restock_success.html", {"username": username}) 

        materials = Store.objects.get(user = valid_token_user).material_entries.exclude(max_capacity = F("current_capacity")).values()
        total_price = 0
        for material in materials:
            material.update({"restock_capacity": (material['max_capacity'] - material['current_capacity'])})
            total_price += material['price'] * material["restock_capacity"]

    return render(request, "store/restock.html", {"username": username, "materials": materials, "total_price": total_price})

def sales_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        track_current_quantity = {}
        choices = [(product.id, product.product_name) for product in Product.objects.all()]
        sales_forms = [SalesForm(track_current_quantity, choices)]

        if request.method == "POST":
            products = request.POST.getlist("product")
            quantities = request.POST.getlist("quantity")
            sales_form_error_flag = False

            sales_forms = []
            for product_id, product_quantity in zip(products, quantities):
                sales_form = SalesForm(track_current_quantity, choices, data = {"product": product_id, "quantity": product_quantity})
                sales_forms.append(sales_form)

                if not sales_form.is_valid():
                    sales_form_error_flag = True
                    continue

            if not sales_form_error_flag and len(sales_forms):
                for material_id in track_current_quantity.keys():
                    material = Material.objects.get(pk = material_id)
                    material.current_capacity = track_current_quantity[material_id]
                    material.save()

                return render(request, "store/sales_success.html", {"username": username})
            
    return render(request, "store/sales.html", {"username": username, "sales_forms": sales_forms, "choices": choices})