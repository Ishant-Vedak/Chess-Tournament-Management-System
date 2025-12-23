from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from .forms import RegisterUser
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.

def user(request):
    return HttpResponse("This is a sample user")

def all_users(request):
    users = User.objects.all()

    context = {
        "users": users
    }

    return render(request, "users/overview.html", context)

def create_user(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterUser()

    return render(request, "users/create_user.html", {"form": form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("admin:index")
        return reverse_lazy("dashboard")