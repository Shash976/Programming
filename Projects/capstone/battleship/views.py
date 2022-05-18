from django.shortcuts import render

# Create your views here.

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

def play_game(request, player1, player2):
    pass