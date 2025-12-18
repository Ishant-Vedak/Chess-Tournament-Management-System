from django.urls import path
from . import views

app_name = "clubs"
urlpatterns = [
    path("", views.club, name="landing_page"),
    path("all/", views.all_clubs, name="all_clubs"),
    path("all/<uuid:uuid>/", views.club_details, name="club_details")
]