from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    ids = len(Flight.objects.all())
    if flight_id <= ids:
        flight = Flight.objects.get(id=flight_id)
        passengers = flight.passengers.all()
        return render(request, "flights/flight.html", {
            "flight":flight,
            "passengers": passengers,
            "non_passengers":Passenger.objects.exclude(flights=flight).all()
        })
    else:
        return render(request, "flights/error.html")

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(id=flight_id)
        passenger = Passenger.objects.get(id=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))