from django.shortcuts import render, redirect
from .forms import LoginForm, NewUserForm

def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "user/login.html", {"form": form})

def new_user_page(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(data = request.POST)
        if form.is_valid():
            form.save()
            return render(request, "user/success.html")

    return render(request, "user/new_user.html", {"form": form})