import json
import os
import re
import smtplib
import time

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from .convert import *
from .forms import *
from .models import *


# Create your views here.

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
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")

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
            return render(request, "main/register.html", {"message": "Passwords must match."})
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "main/register.html", {"message": "Username already taken."})  
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/register.html")

def index(request):
    if request.method == "POST":
        form = NewEmailForm(request.POST, request.FILES)
        if form.is_valid():
            body = form.cleaned_data["content"]
            subject = form.cleaned_data["subject"]
            recipients = form.cleaned_data["recipients"]
        mail = Mail.objects.create(user=request.user, file=recipients, body=body)
        mail.save
        recipients_tuple = get_recipients(mail.file)
        process_email(content=body, subject=subject)
    return render(request, "main/index.html", {
        "form": NewEmailForm(),
        })


def get_recipients(json_file):
    with open(json_file.path) as file:
        data = json.loads(file.read())
    return data

    untouched = content
    recipients = to.strip().split(',')
    for recipient in recipients:
        content = untouched
        recipient=recipient.strip()
        person = Recipient.objects.get(email=recipient).serialize()
        results = re.findall(r'`(\w+)`', content)
        for result in results:
            content = re.sub(f'`{result}`', person[result], content)
        server_ssl.sendmail("itshashgoel@gmail.com", recipient, content)
    server_ssl.quit()

def get_recipients(filepath):
    if re.search(r'.xslx$', filepath):
        json_file = excel_to_json(filepath)
    elif re.search(r'.csv$', filepath):
        json_file = csv_to_json(filepath)
    elif re.search(r'.json$', filepath):
        json_file = filepath

    with open(json_file) as file:
        data = json.load(file)

def process_email(content, subject, recipients):    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.connect("smtp.gmail.com",465)
    server.ehlo()
    server.login("itshashgoel@gmail.com", "superuchihalevidino")
    recipients = get_recipients(mail.json_file)
    vars = ('|').join([var for var in recipients[0].keys()])
    results = re.findall(f'`({vars})`', mail.body)
    for recipient in recipients:
        content = untouched
        results = re.findall(r'`(\w+)`', content)
        for result in results:
            content = re.sub(f'`{result}`', recipient[result], content)
        server.sendmail("itshashgoel@gmail.com", "shashwat.stanford@gmail.com", content)
        time.sleep(1)
    server.quit()
