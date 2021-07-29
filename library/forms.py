from django import forms
from django.forms.widgets import Textarea

class TicketCreationForm(forms.Form):

    title = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'size': 128}))
    description = forms.CharField(label='Description', max_length=2048, widget=forms.Textarea(attrs={'cols': 130}))
    image = forms.ImageField(label="Image", required=False)
