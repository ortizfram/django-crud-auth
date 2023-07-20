from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# exe smt when URL is visited
def helloworld(request):
    return render(request, "signup.html", {"form": UserCreationForm})
