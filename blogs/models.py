import os

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.category_name}"


STATUS_CHOICES = (
    ("Draft", "Draft"),
    ("Published", "Published"),
)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="upload/%Y/%m/%d")
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=5000)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Draft")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"

    def delete(self, *args, **kwargs) -> None:
        # Delete the file associated with the model instance
        if self.featured_image:
            if os.path.isfile(self.featured_image.path):
                os.remove(self.featured_image.path)
        super(Blog, self).delete(*args, **kwargs)
