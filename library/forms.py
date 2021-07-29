from django import forms

class TicketCreationForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=128)
    description = forms.CharField(label='Description', max_length=2048)
    image = forms.ImageField(label="image", )
