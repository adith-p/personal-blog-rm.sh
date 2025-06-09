from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="bloglist"),
    path("add/", views.add_post, name="addPost"),
    path("article/<str:file_id>/", views.read_post, name="readPost"),
    path("edit/<str:file_id>/", views.update_post, name="editPost"),
    path("delete/<str:file_id>/", views.delete_post, name="deletePost"),
]
