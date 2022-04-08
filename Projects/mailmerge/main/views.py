from operator import concat
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import NewEmailForm, NewRecipientForm
from .models import Recipient

import re
import smtplib

# Create your views here.

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
    rc = {}
    recipients = to.strip().split(',')
    for recipient in recipients:
        content = untouched
        recipient=recipient.strip()
        person = Recipient.objects.get(email=recipient)
        cp = r'`(\w+)`'
        results = re.findall(cp, content)
        for result in results:
            omit = f'`{result}`'
            if result == 'first_name':
                content = re.sub(omit, person.first_name, content)
            elif result == 'last_name':
                content = re.sub(omit, person.last_name, content)
            elif result == 'email':
                content = re.sub(omit, person.email, content)
            elif result == 'address':
                content = re.sub(omit, person.address, content)
        dict = {recipient: content}
        rc.update(dict)
        server_ssl.sendmail("itshashgoel@gmail.com", recipient, content)
    server_ssl.quit()