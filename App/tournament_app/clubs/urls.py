from django.urls import path
from . import views

app_name = "clubs"
urlpatterns = [
    path("", views.club, name="landing_page")
]