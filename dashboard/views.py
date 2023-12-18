import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from blogs.models import Blog, Category

from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
def add_category(request: HttpRequest) -> render or redirect:
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
        else:
            logging.error(form.errors)
    form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)


# "dashboard/categories/edit/<blog_id>"
@login_required(login_url="login")
def edit_category(request: HttpRequest, category_id: int) -> render or redirect:
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
        else:
            logging.error(form.errors)
    form = CategoryForm(instance=category)
    context = {
        "category": category,
        "form": form,
    }
    return render(request, "dashboard/edit_category.html", context)


# "dashboard/categories/edit/<blog_id>"
@login_required(login_url="login")
def delete_category(request: HttpRequest, category_id: int) -> redirect or redirect:
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect("dashboard_categories")


# "dashboard/blogs"
@login_required(login_url="login")
def blogs(request: HttpRequest) -> render:
    blogs = Blog.objects.all()
    context = {"blogs": blogs}
    return render(request, "dashboard/blogs.html", context)


# "dashboard/blogs/add"
@login_required(login_url="login")
def add_blog(request: HttpRequest) -> render or redirect:
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            form.save()
            title = form.cleaned_data["title"]
            blog.slug = f"{slugify(title)}-{blog.id}"
            blog.save()
            return redirect("dashboard_blogs")
        else:
            logging.error(form.errors)
    form = BlogPostForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/add_blog.html", context)


# "dashboard/blogs/edit/<blog_id>"
@login_required(login_url="login")
def edit_blog(request: HttpRequest, blog_id: int) -> render or redirect:
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save()
            title = form.cleaned_data["title"]
            blog.slug = f"{slugify(title)}-{blog.id}"
            blog.save()
            return redirect("dashboard_blogs")
        else:
            logging.error(form.errors)
    form = BlogPostForm(instance=blog)
    context = {
        "blog": blog,
        "form": form,
    }
    return render(request, "dashboard/edit_blog.html", context)


# "dashboard/categories/delete/<blog_id>"
@login_required(login_url="login")
def delete_blog(request: HttpRequest, blog_id: int) -> redirect or redirect:
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect("dashboard_blogs")


# "dashboard/users"
@permission_required("dashboard.view_user")
@login_required(login_url="login")
def users(request: HttpRequest) -> render:
    users = User.objects.all()
    context = {"users": users}
    return render(request, "dashboard/users.html", context)


# "dashboard/users/add"
@permission_required("dashboard.add_user")
@login_required(login_url="login")
def add_user(request: HttpRequest) -> render or redirect:
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_users")
        else:
            logging.error(form.errors)
    form = AddUserForm()
    context = {"form": form}
    return render(request, "dashboard/add_user.html", context)


# "dashboard/users/edit/<user_id>"
@permission_required("dashboard.change_user")
@login_required(login_url="login")
def edit_user(request: HttpRequest, user_id) -> render or redirect:
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard_users")
        else:
            logging.error(form.errors)
    form = EditUserForm(instance=user)
    context = {
        "user": user,
        "form": form,
    }
    return render(request, "dashboard/edit_user.html", context)


# "dashboard/categories/delete/<blog_id>"
@permission_required("dashboard.delete_user")
@login_required(login_url="login")
def delete_user(request: HttpRequest, user_id: int) -> redirect:
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect("dashboard_users")
