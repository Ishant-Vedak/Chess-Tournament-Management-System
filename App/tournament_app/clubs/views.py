from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Club

# Create your views here.

def club(request):
    return HttpResponse("this is a sample club")

def all_clubs(request):
    clubs = Club.objects.all()
    context = {
        "clubs": clubs
    }
    return render(request, "clubs/overview.html", context)

def club_details(request, uuid):
    club = get_object_or_404(Club, uuid=uuid)
    context = {
        "club": club
    }
    return render(request, "clubs/detail.html", context)