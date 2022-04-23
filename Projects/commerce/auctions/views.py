from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data["description"]
            title = form.cleaned_data["listing_title"]
            starting_bid = form.cleaned_data["bid"]
            user = request.user
            image = form.cleaned_data["image"]
            category = Category.objects.get(id=int(request.POST["category"]))
        listing=Listing.objects.create(title=title, description=description, bid=starting_bid, seller=user, image=image)
        listing.save
        category.listings.add(listing)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "form": NewListingForm(),
        "categories": Category.objects.all(),
        "red": None,
        })

def listing(request, listing_id):
    item_details = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        bid = request.POST.get("bid")
        if request.user.is_authenticated:
            item = Listing.objects.get(pk=listing_id)
            user=request.user
            if int(bid) <= item.bid:
                return render(request, "auctions/listing.html", {"listing":item_details})
            item.bid = int(bid)
            item.save()
            return HttpResponseRedirect(reverse('listing', args=(item.id,)))
    return render(request, "auctions/listing.html", {"listing":item_details})


def categories(request):
    return render(request, "auctions/categories.html", {"categories": Category.objects.all()})

def category(request, category):
    c = Category.objects.get(category=category)
    listings = c.listings.all()
    return render(request, "auctions/category.html", {"category":c, "listings":listings})

def watchlist(request):
    pass