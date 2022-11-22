from django.shortcuts import render, redirect
from .forms import LoginForm, INVALID_USERNAME_ERROR
from .models import User

# Create your views here.
def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "user/login.html", {"form": form})