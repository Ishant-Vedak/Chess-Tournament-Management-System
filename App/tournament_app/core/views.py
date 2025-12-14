from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def landing_page(request):
    testing = "This is a landing page"
    return HttpResponse(testing)
