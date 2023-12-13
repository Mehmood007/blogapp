from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
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
]
