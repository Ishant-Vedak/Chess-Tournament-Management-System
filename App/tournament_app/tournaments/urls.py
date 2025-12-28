from django.urls import path
from . import views

app_name = "tournaments"
urlpatterns = [
    path("", views.tournament, name="tournament"),
    path("all/", views.all_tournaments, name="all_tournaments"),
    path('all/<uuid:uuid>/', views.tournament_details, name='tournament_details'),
    path("create/", views.create_tournament, name="create_tournament"),
    path("join/", views.join_tournament, name="join_tournament"),
    path("my_tournaments/", views.my_tournaments, name="my_tournaments"),
]