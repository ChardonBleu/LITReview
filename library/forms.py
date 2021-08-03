from django import forms
from .models import Ticket

class TicketCreationForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'image']
