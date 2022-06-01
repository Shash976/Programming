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

def updateInGamePlayer(request,match_id,username):
    user = User.objects.get(username=username)
    game = Match.objects.get(id=match_id)
    player = PlayerInGame.objects.get(user=user, match=game)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('turns'):
            player.turns = int(data['turns'])
        if data.get('hits'):
            player.hits = int(data['hits'])
        if data.get('opponentMap'):
            users = list(player.match.players.all())
            opponent_player = PlayerInGame.objects.get(user = users[~users.index(player.user)], match=game)
            opponent_player.inGameMap = json.dumps(data.get('opponentMap')).strip()
        if data.get('type'):
            if data.get('type').strip().upper() == "WINNER":
                player.type = player.WINNER
                game.winner=player.user
            elif data.get('type').strip.upper() == "LOSER":
                player.type = player.LOSER
            else:
                player.type = player.UKNOWN
        game.save()
        player.save()
    elif request.method == "POST":
        return JsonResponse({"message":"GET or PUT request please"})
    return JsonResponse(player.serialize())

@login_required(login_url=reverse_lazy("battleship:login"))
def create_match(request, match_id=None):
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

def getMatch(request, match_id):
    return JsonResponse(Match.objects.get(id=match_id).serialize())

@login_required(login_url=reverse_lazy("login"))
@csrf_exempt
def play(request):
    p1 = User.objects.get(username=request.GET.get('p1').strip())
    p2 = User.objects.get(username=request.GET.get('p2').strip())
    p1m = json.dumps(json.loads(request.GET.get('p1m').strip()))
    p2m = json.dumps(json.loads(request.GET.get('p2m').strip()))
    u1m = max([list(p1.maps.all()).index(m) for m in p1.maps.filter(map=p1m)])
    u2m = max([list(p2.maps.all()).index(m) for m in p2.maps.filter(map=p2m)])
    players = {"p1":p1.username,"p1m":u1m, "p2":p2.username, "p2m":u2m}
    return HttpResponseRedirect(reverse("battleship:game", kwargs={"players":("").join(json.dumps(players).split())}))

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