from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from blogs.models import Blog, Category


# "/" # home route
def home(request: HttpRequest) -> render:
    featured_posts = Blog.objects.filter(is_featured=True, status=1)
    posts = Blog.objects.filter(is_featured=False, status=1)
    context = {
        "featured_posts": featured_posts,
        "posts": posts,
    }
    return render(request, "home.html", context)


# register/ # Sign Up page
def register(request: HttpRequest) -> render:
    return HttpResponse("Sign Up page here")
