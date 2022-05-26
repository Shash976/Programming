from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

import json

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
            return HttpResponseRedirect(reverse("battleship:index"))
        else:
            return render(request, "battleship/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "battleship/login.html")

@login_required(login_url=reverse_lazy("battleship:login"))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("battleship:index"))

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

@login_required(login_url=reverse_lazy("battleship:login"))
def index(request):
    if request.method == "POST":
        pass
    return render(request, "battleship/index.html", {"players":User.objects.exclude(username=request.user.username).all()})

def map_api(request, map_id):
    map = Map.objects.get(id=map_id)
    return JsonResponse(map.serialize())

@login_required(login_url=reverse_lazy("battleship:login"))
@csrf_exempt
def create_map(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("player")
        map = data.get("map")
        i = data.get("index")
        m = Map.objects.create(user=User.objects.get(username=username), map=map)
        m.save()
        return JsonResponse({"message": f"Worked. Index is {i}"})
    else:
        return JsonResponse({"message": "Please send POST request"})

@login_required(login_url=reverse_lazy("login"))
@csrf_exempt
def play(request):
    p1 = request.GET.get('p1').strip()
    p1m = request.GET.get('p1m').strip()
    p2 = request.GET.get('p2').strip()
    p2m = request.GET.get('p2m').strip()
    u1m = max([m.id for m in Map.objects.filter(map=(', ').join(p1m.split(',')))])
    u2m = max([m.id for m in Map.objects.filter(map=(', ').join(p2m.split(',')))])
    players = {"p1":p1,"p1m":u1m, "p2":p2, "p2m":u2m}
    return HttpResponseRedirect(reverse("battleship:game", kwargs={"players":json.dumps(players)}))

def game(request, players):
    players = json.loads(players)
    game = Match.objects.create()
    game.save()
    p1 = PlayerInGame.objects.create(user = User.objects.get(username=players["p1"]), match=game, type='UNKNOWN')
    p2 = PlayerInGame.objects.create(user = User.objects.get(username=players["p2"]), match=game, type='UNKNOWN')
    p1.save()
    p2.save()
    p1m = Map.objects.get(id=players["p1m"])
    p2m = Map.objects.get(id=players["p2m"])
    return render(request, "battleship/play.html", {"match": game})