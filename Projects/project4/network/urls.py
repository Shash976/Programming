
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .models import *

users = f"({('|').join([user.username for user in User.objects.all()])})"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),

    #Regex Paths
    re_path(r'posts/(\d+)', views.likes, name="likes"), #(API Route)
    re_path(users, views.profile, name="profile")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

