from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

# Create your views here.
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

tasks = []
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "arctic/index.html", {"tasks": request.session["tasks"], "tb": len(tasks)!=0})

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("arctic:index"))
        else:
            return render(request, "arctic/add.html", {"form": form})

    return render(request, "arctic/add.html", {"form": NewTaskForm()})