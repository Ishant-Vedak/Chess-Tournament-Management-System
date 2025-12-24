from django.urls import path
from . import views

app_name = "tournaments"
urlpatterns = [
    path("", views.tournament, name="tournament"),
    path("all/", views.all_tournaments, name="all_tournaments"),
    path("my_tournaments/", views.my_tournaments, name="my_tournaments"),
]