from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm, NewUserForm
from .models import User, Token

def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        if user is not None:
            try:
                token = Token.objects.get(user = user)
            except Token.DoesNotExist:
                token = Token.objects.create(user = user)
        
            response = redirect(f"{username}/home/")
            response['token'] = token
            auth_login(request, user)
            
            return response
            
    return render(request, "user/login.html", {"form": form})

def new_user_page(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(data = request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            User.objects.create_user(username = username, password = password)
            return render(request, "user/success.html")

    return render(request, "user/new_user.html", {"form": form})

def logout(request):
    auth_logout(request)
    return redirect('/')
