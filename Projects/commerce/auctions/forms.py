from django import forms
from .models import *

class NewListingForm(forms.Form):
    listing_title=forms.CharField(label="Enter Title")
    bid = forms.IntegerField(label="Starting Bid: $")
    description=forms.CharField(widget=forms.Textarea, label="Add Description")
    image = forms.ImageField(required=False)