
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import NewPostForm
from .models import User, Post
import datetime
from operator import attrgetter


def index(request):
    posts = Post.objects.all().order_by('-id')
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts":page_obj})

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, first_name, last_name, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data["description"]
            username = request.user
            image = form.cleaned_data["image"]
        post=Post.objects.create(content=description, user=username, time=datetime.datetime.now(), image=image, likes=0)
        post.save
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/newpost.html", {
        "form": NewPostForm(),
        })

def profile(request, username):        
    if request.method == "POST":
        account = User.objects.get(username=username)
        current_user = request.user
        data = request.POST
        action = data.get("follow")
        if action == "Follow":
            current_user.follows.add(account)
        elif action == "Unfollow":
            current_user.follows.remove(account)
        current_user.save()
    if username in str(User.objects.all()):
        user = User.objects.get(username=username)
        posts = user.posts.all().order_by('-id')

        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/profile.html', {'profile': user, 'posts':page_obj})
    else:
        return HttpResponse('User Does not Exist')

def following(request):
    user = request.user
    accounts = user.follows.all()
    posts = []
    for account in accounts:
        posts.extend(account.posts.all())
    res = sorted(posts, key=attrgetter('id'), reverse=True)
    paginator = Paginator(res, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts":page_obj})