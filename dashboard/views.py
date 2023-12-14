import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from blogs.models import Blog, Category

from .forms import BlogPostForm, CategoryForm

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
def add_category(request: HttpRequest) -> render:
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
def edit_category(request: HttpRequest, category_id: int) -> render:
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
def delete_category(request: HttpRequest, category_id: int) -> redirect:
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
def add_blog(request: HttpRequest) -> render:
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
def edit_blog(request: HttpRequest, blog_id: int) -> render:
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
def delete_blog(request: HttpRequest, blog_id: int) -> redirect:
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect("dashboard_blogs")
