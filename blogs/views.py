from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import Blog, Category, Comment


# category/<category_id>
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


# blogs/search/?keyword=<searched_keyword>
def search(request: HttpRequest) -> render:
    keyword = request.GET.get("keyword")
    blogs = Blog.objects.filter(
        Q(title__icontains=keyword)
        | Q(short_description__icontains=keyword)
        | Q(blog_body__icontains=keyword),
        status="Published",
    )
    context = {
        "keyword": keyword,
        "blogs": blogs,
    }
    return render(request, "search.html", context)
