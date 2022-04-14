from django import forms

class NewEmailForm(forms.Form):
    recipient_csv = forms.FileField(required=False, label="Upload Sheet")
    to = forms.CharField(label = "Recipients")
    subject = forms.CharField(label="Subject", required=False)
    content = forms.CharField(widget=forms.Textarea, label="Message")

class NewRecipientForm(forms.Form):
    first_name = forms.CharField(max_length=35)
    last_name = forms.CharField(max_length=35, required=False)
    email = forms.EmailField()
    address = forms.CharField(max_length=500, required=False)