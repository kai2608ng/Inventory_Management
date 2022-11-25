from django.shortcuts import render

# Create your views here.
def home_page(request, username):
    return render(request, "store/home.html")