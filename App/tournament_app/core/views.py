from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def landing_page(request):
    return render(request, "core/index.html")

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")