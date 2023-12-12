from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Blog, Category


def posts_by_category(request: HttpRequest, category_id: int) -> render:
    posts = Blog.objects.filter(status=1, category=category_id)
    category = get_object_or_404(Category, pk=category_id)
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "posts_by_category.html", context)


def blog(request: HttpRequest, slug: str) -> render:
    post = get_object_or_404(
        Blog.objects.select_related("category"), slug=slug, status=1
    )
    context = {"post": post}
    return render(request, "blog.html", context)
