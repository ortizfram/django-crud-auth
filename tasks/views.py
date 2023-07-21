from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError


# exe smt when URL is visited
def home(request):
    return render(request, "home.html")


# the form comes from this same file
def signup(request):
    if request.method == "GET":
        # send signup page
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        # if same password Register User
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            # User already exists
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists"},
                )
        # password does not match
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password do not match"},
        )


def tasks(request):
    return render(request, "tasks.html")
