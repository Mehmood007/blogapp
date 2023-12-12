from django.http import HttpRequest
from django.shortcuts import render

from blogs.models import Blog, Category


def home(request: HttpRequest) -> render:
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status=1)
    posts = Blog.objects.filter(is_featured=False, status=1)
    context = {
        "categories": categories,
        "featured_posts": featured_posts,
        "posts": posts,
    }
    return render(request, "home.html", context)
