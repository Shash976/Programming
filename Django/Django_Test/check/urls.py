from django.urls import path
from . import views

urlpatterns = [
    path("", views.html, name="Index"),
    path("bday", views.bday, name="bday"),
    #path("<str:name>", views.greet, name="Greet"),
]
