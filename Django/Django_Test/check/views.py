from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def index(request):
    return HttpResponse("Hello!")

def greet(request, name):
    return render(request, "check/greet.html", {"name": name.capitalize()})

def html(request):
    return render(request, "check/index.html")

def bday(request):
    now = datetime.datetime.now()
    if now.month == 9 and now.day == 22:
        ans = "Yes"
    else:
        ans = "No"
    return render(request, "check/bday.html", {"ans":ans})