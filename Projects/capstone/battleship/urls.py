from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .models import *

app_name = "battleship"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    #APIs
    path("maps/create", views.create_map, name="create_map")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)