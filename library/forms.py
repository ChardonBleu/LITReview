from django import forms
from .models import Ticket, Review

class TicketCreationForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'image']

class ReviewCreationForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['headline',
                  'body',
                  'rating']
