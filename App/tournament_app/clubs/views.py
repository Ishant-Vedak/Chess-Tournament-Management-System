from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    return render(request, "clubs/detail.html", {"club": club})

@login_required
def my_club(request):
    clubs = request.user.clubs.all()
    return render(request, 'clubs/user_clubs.html', {"clubs": clubs})

@login_required
def join_club(request):
    ...

@login_required
def create_club(request):
    ...