from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Club, ClubMembership
from .forms import CreateClub

# Create your views here.

def club(request):
    return HttpResponse("this is a sample club")

def all_clubs(request):
    clubs = Club.objects.all()
    return render(request, "clubs/overview.html", {"clubs": clubs})

def club_details(request, uuid):
    club = get_object_or_404(Club, uuid=uuid)
    return render(request, "clubs/detail.html", {"club": club})

@login_required
def my_clubs(request):
    clubs = request.user.clubs.all()
    return render(request, 'clubs/user_clubs.html', {"clubs": clubs})

@login_required
def join_club(request):
    ...

@login_required
def create_club(request):
    if request.method == "POST":
        form = CreateClub(request.POST)
        if form.is_valid():
            user = request.user
            club_name = form.cleaned_data['club_name']
            website = form.cleaned_data['website']
            club = Club(name=club_name, website=website)
            club.save()
            membership = ClubMembership(user=user, club=club, role='FOUNDER')
            membership.save()
            return redirect('dashboard')
    else:
        form = CreateClub()
    return render(request, 'clubs/create_club.html', {'form': form})