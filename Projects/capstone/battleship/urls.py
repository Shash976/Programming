from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .models import *

app_name = "battleship"

urlpatterns = [
    path("", views.index, name="index"),

    # Authentication
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    # APIs
    path("matches/create/<int:match_id>", views.create_match, name="create_match"),
    path("matches/create", views.create_match, name="create_match"),
    path("matches/<int:match_id>/<str:username>", views.updateInGamePlayer, name="maps"),
    path("matches/<int:match_id>", views.getMatch, name="getMatch"),

    # GAME
    path("play", views.play, name="play"),
    path("gameover", views.gameover, name="gameover")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)