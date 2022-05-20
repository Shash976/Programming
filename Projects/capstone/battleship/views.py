from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "battleship/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "battleship/login.html")

@login_required(login_url=reverse_lazy("login"))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "battleship/register.html", {"message": "Passwords must match."})
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "battleship/register.html", {"message": "Username already taken."})  
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "battleship/register.html")

@login_required(login_url=reverse_lazy("login"))
def index(request):
    if request.method == "POST":
        pass
    return render(request, "battleship/index.html", {"players":User.objects.exclude(username=request.user.username).all()})

@login_required(login_url=reverse_lazy("login"))
@csrf_exempt
def create_map(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("user")
        map = data.get("map")
        m = Map.objects.create(user=User.objects.get(username=username), map=map)
        m.save()
        return JsonResponse({"message": "It worked successfully."}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@login_required(login_url=reverse_lazy("login"))
@csrf_exempt
def play_game(request, player1, player2):
    pass