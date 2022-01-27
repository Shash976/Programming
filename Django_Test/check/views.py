from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello!")

def greet(request, name):
    return HttpResponse(f"Hi, {name.capitalize()}")

def html(request):
    return render(request, "check/index.html")