from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from .forms import MaterialForm
from store.models import Store
from .models import Material

def stupid_authentication(request):
    token = request.session.get('token', None)
    return authenticate(request, token = token)

def material_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        materials = Store.objects.get(user = valid_token_user).material_entries.all()
        return render(request, "material/material.html", {'username': username, "materials": materials})

    return redirect(reverse("login_page"))

def new_material_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        store = Store.objects.get(user = valid_token_user)
        form = MaterialForm()

        if request.method == "POST":
            data = {
                "material_name": request.POST['material_name'],
                "price": request.POST['price'],
                "max_capacity": request.POST["max_capacity"],
                "current_capacity": request.POST["current_capacity"],
                "store": store
            }
            form = MaterialForm(data = data)
            if form.is_valid():
                form.save()

        return render(request, "material/new_material.html", {"username": username, "form": form})

def edit_material_page(request, username, material_id):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        material = Material.objects.get(pk = material_id)
        intial_data =  {
            "material_name": material.material_name,
            "price": material.price,
            "max_capacity": material.max_capacity,
            "current_capacity": material.current_capacity
        }
        form = MaterialForm(initial = intial_data)

        if request.method == "POST":
            store = Store.objects.get(user = valid_token_user)
            data = {
                "material_name": request.POST['material_name'],
                "price": request.POST['price'],
                "max_capacity": request.POST["max_capacity"],
                "current_capacity": request.POST["current_capacity"],
                "store": store
            }
            form = MaterialForm(data = data, instance = material)
            if form.is_valid():
                form.save()

        form.fields["material_name"].widget.attrs["readonly"] = True
        form.fields["price"].widget.attrs["readonly"] = True
        form.fields["current_capacity"].widget.attrs["readonly"] = True

        return render(request, "material/edit_material.html", {"username": username, "material_id": material_id, "form": form})

def delete_material_page(request, username, material_id):
    try:
        material = Material.objects.get(pk = material_id)
        material.delete()
    except Material.DoesNotExist:
        return render(request, "material/material_error.html", {"username": username})

    return redirect(reverse("material_page", args = (username, )))