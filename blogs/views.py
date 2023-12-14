from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import Blog, Category, Comment


# cateogry/<category_id>
def posts_by_category(request: HttpRequest, category_id: int) -> render:
    posts = Blog.objects.filter(status="Published", category=category_id)
    category = get_object_or_404(Category, pk=category_id)
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "posts_by_category.html", context)


# blog/<blog-slug>
def blog(request: HttpRequest, slug: str) -> render:
    post = get_object_or_404(
        Blog.objects.select_related("category"), slug=slug, status="Published"
    )
    if request.method == "POST":
        comment = Comment()
        comment.author = request.user
        comment.blog = post
        comment.comment = request.POST["comment"]
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(blog=post)
    comments_count = comments.count()
    context = {
        "post": post,
        "comments": comments,
        "comments_count": comments_count,
    }
    return render(request, "blog.html", context)


# blogs/search/?keyword=<serached_keyword>
def search(request: HttpRequest) -> render:
    keword = request.GET.get("keyword")
    blogs = Blog.objects.filter(
        Q(title__icontains=keword)
        | Q(short_description__icontains=keword)
        | Q(blog_body__icontains=keword),
        status=1,
    )
    context = {
        "keyword": keword,
        "blogs": blogs,
    }
    print(blogs)
    return render(request, "search.html", context)
