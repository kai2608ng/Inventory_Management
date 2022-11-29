from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from .models import Store
from .forms import StoreForm

User = get_user_model()

def user_authentication(request):
    token = request.session.get("token", None)
    valid_token_user = authenticate(request, token = token)
    return request.user.is_authenticated and valid_token_user

def home_page(request, username):
    if user_authentication(request):
        store = Store.objects.filter(user = request.user)
        return render(request, "store/home.html", {'username': username, 'store': store})

    return redirect(reverse("login_page"))

def new_store_page(request, username):
    form = StoreForm()

    if request.method == "POST":
        store_name = request.POST["store_name"]
        form = StoreForm(data = {"store_name": store_name, "user": request.user})
        if form.is_valid():
            form.save()
            return redirect(reverse('home_page', args = (username, )))

    return render(request, "store/new_store.html", {"username": username, "form": form})

def store_detail_page(request, username, store_name):
    if user_authentication(request):
        return render(request, "store/store_detail.html")
    