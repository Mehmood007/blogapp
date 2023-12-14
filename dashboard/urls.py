from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Categories CRUD
    path("categories", views.categories, name="dashboard_categories"),
    path("categories/add", views.add_category, name="add_category"),
    path(
        "categories/edit/<int:category_id>", views.edit_category, name="edit_category"
    ),
    path(
        "categories/delete/<int:category_id>",
        views.delete_category,
        name="delete_category",
    ),
    # Blogs CRUD
    path("blogs", views.blogs, name="dashboard_blogs"),
    path("blogs/add", views.add_blog, name="add_blog"),
    path("blogs/edit/<int:blog_id>", views.edit_blog, name="edit_blog"),
    path(
        "blogs/delete/<int:blog_id>",
        views.delete_blog,
        name="delete_blog",
    ),
]
