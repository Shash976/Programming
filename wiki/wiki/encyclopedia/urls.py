from django.urls import path, re_path
from . import views


app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name="search"),
    re_path(r"^(?P<title>\w+)$", views.entry, name="entry"),
]
