from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import LoginForm, NewUserForm
from .models import User, Token

def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            token = Token.objects.create(user = user)
            response = render(request, "user/login.html", {"form": form})
            response['token'] = token
            return response
            
    return render(request, "user/login.html", {"form": form})

def new_user_page(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(data = request.POST)
        if form.is_valid():
            form.save()
            return render(request, "user/success.html")

    return render(request, "user/new_user.html", {"form": form})


def test_view(request):
    pass