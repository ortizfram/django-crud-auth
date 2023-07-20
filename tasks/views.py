from django.shortcuts import render
from django.http import HttpResponse


# exe smt when URL is visited
def helloworld(request):
    return HttpResponse("hello world")
