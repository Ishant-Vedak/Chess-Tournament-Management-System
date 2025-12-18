from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def landing_page(request):
    testing = {"1": "This is a sample message"}
    return render(request, "core/index.html", {"testing": testing})
