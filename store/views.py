from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from .models import Store
from .forms import StoreForm

User = get_user_model()

def stupid_authentication(request):
    token = request.session.get('token', None)
    return authenticate(request, token = token)

def home_page(request, username):
    valid_token_user = stupid_authentication(request)
    
    if valid_token_user:
        auth_login(request, valid_token_user)
        store = Store.objects.filter(user = request.user)
        return render(request, "store/home.html", {'username': username, 'store': store})

    return redirect(reverse("login_page"))

def new_store_page(request, username):
    valid_token_user = stupid_authentication(request)
    if valid_token_user:
        form = StoreForm()

        if request.method == "POST":
            store_name = request.POST["store_name"]
            form = StoreForm(data = {"store_name": store_name, "user": request.user})
            if form.is_valid():
                form.save()
                return redirect(reverse('home_page', args = (username, )))

        return render(request, "store/new_store.html", {"username": username, "form": form})
    
    return redirect(reverse("login_page"))
    