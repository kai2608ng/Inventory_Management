from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from .forms import MaterialForm

def stupid_authentication(request):
    token = request.session.get('token', None)
    return authenticate(request, token = token)

def material_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        return render(request, "material/material.html", {'username': username})

    return redirect(reverse("login_page"))

def new_material_page(request, username):
    valid_token_user = stupid_authentication(request)

    if valid_token_user:
        return render(request, "material/new_material.html", {"username": username})