from django.shortcuts import render

# Create your views here.

def login():
    context = {}
    return render("login/login.html", context)

def landing(request):
    context = {}
    return render("login/landing.html", context)
