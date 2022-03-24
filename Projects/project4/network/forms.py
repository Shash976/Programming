from django import forms
from .models import *

class NewPostForm(forms.Form):
    description=forms.CharField(widget=forms.Textarea, label="Add Description")
    image = forms.ImageField(required=False)