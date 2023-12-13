from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog, Category

from .forms import CategoryForm


# "dashboard/"
@login_required(login_url="login")
def dashboard(request: HttpRequest) -> render:
    categories_count = Category.objects.all().count()
    posts_count = Blog.objects.all().count()
    context = {
        "categories_count": categories_count,
        "posts_count": posts_count,
    }
    return render(request, "dashboard/dashboard.html", context)


# "dashboard/categories"
@login_required(login_url="login")
def categories(request: HttpRequest) -> render:
    return render(request, "dashboard/categories.html")


# "dashboard/categories/add"
@login_required(login_url="login")
def add_category(request: HttpRequest) -> render:
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
    form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)


# "dashboard/categories/edit/<blog_id>"
@login_required(login_url="login")
def edit_category(request: HttpRequest, category_id: int) -> render:
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
    form = CategoryForm(instance=category)
    context = {
        "category": category,
        "form": form,
    }
    return render(request, "dashboard/edit_category.html", context)


# "dashboard/categories/edit/<blog_id>"
@login_required(login_url="login")
def delete_category(request: HttpRequest, category_id: int) -> redirect:
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect("dashboard_categories")
