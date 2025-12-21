from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("", views.user, name="user"),
    path("all/", views.all_users, name="all_users"),
    path("create/", views.create_user, name="create_users"),
]