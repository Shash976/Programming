from django import forms

class NewEmailForm(forms.Form):
    subject = forms.CharField(label="Subject", required=False)
    content = forms.CharField(widget=forms.Textarea, label="Message")
    recipients = forms.FileField(required=True, label="Recipients")