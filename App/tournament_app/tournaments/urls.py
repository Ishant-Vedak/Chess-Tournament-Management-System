from django.urls import path
from . import views

app_name = "tournaments"
urlpatterns = [
    path("", views.tournament, name="tournament"),
    path("all/", views.all_tournaments, name="all tournaments"),
]