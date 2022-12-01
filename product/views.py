from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from .forms import ProductForm
from store.models import Store

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
        form = ProductForm()
        if request.method == "POST":
            product_name = request.POST['product_name']
            store = Store.objects.get(user = valid_token_user)
            form = ProductForm(data = {'product_name': product_name, 'store': store})
            if form.is_valid():
                form.save()
            
        return render(request, "product/new_product.html", {"username": username, 'form': form})

    return redirect(reverse('login_page'))