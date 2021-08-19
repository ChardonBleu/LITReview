from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    """Used for ticket creation or modification
    Only title is required.

    """
    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'image']

class ReviewForm(forms.ModelForm):
    """Used for review creation or modification
    Headline and rating are required

    """
    class Meta:
        model = Review
        fields = ['headline',
                  'body',
                  'rating']
