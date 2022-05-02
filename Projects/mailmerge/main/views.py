from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import NewEmailForm, NewRecipientForm
from .models import Recipient
from .convert import *

import re
import smtplib
import json

# Create your views here.
'''
def create_recipient(request):
    if request.method == "POST":
        form = NewRecipientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            email = form.cleaned_data["email"]
        new = Recipient.objects.create(first_name=first_name, last_name=last_name, address=address, email=email)
        new.save
        return HttpResponseRedirect(reverse("index"))
    return render(request, "main/index.html", {
        "form": NewRecipientForm(),
        })
'''


def index(request):
    if request.method == "POST":
        form = NewEmailForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            subject = form.cleaned_data["subject"]
            recipients = form.cleaned_data["to"]
        process_email(content=content, subject=subject, to=recipients)
    return render(request, "main/index.html", {
        "form": NewEmailForm(),
        })


def process_email(content, subject, to):    
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.connect("smtp.gmail.com",465)
    server_ssl.ehlo()
    server_ssl.login("itshashgoel@gmail.com", "superuchihalevidino")
    
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

