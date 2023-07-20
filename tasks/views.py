from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        if request.POST["password1"] == request.POST["password1"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                return HttpResponse("User created successfully!")
            except:
                return HttpResponse("Username already exists")
        # send error message: httpResponse
        return HttpResponse("Password do not match")
