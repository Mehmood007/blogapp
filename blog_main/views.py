import logging

from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import redirect, render

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

from blogs.models import Blog

from .forms import RegistrationForm


# "/" # home route
def home(request: HttpRequest) -> render:
    featured_posts = Blog.objects.filter(is_featured=True, status="Published")
    posts = Blog.objects.filter(is_featured=False, status="Published")
    context = {
        "featured_posts": featured_posts,
        "posts": posts,
    }
    return render(request, "home.html", context)


# "register/" # Sign Up page
def register(request: HttpRequest) -> render:
    if request.method == "GET":
        form = RegistrationForm()
        context = {
            "form": form,
        }
        return render(request, "register.html", context)
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            logging.error(form.errors)
            return redirect("register")


# "login"
def login(request: HttpRequest) -> render:
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
            else:
                logging.warning("Authentication failed. Invalid credentials.")
        else:
            logging.error(form.errors)
        return redirect("login")
    else:
        form = AuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "login.html", context)


# logout
def logout(request: HttpRequest) -> render:
    auth.logout(request)
    return redirect("home")
