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

class TicketUpdateForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'image']

    def save(self, commit=True):
        ticket = self.instance
        ticket.title = self.cleaned_data['title']
        ticket.description = self.cleaned_data['description']
        if self.cleaned_data['image']:
            ticket.image = self.cleaned_data['image']
        if commit:
            ticket.save()
        return ticket

class ReviewUpdateForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['headline',
                  'body',
                  'rating']

    def save(self, commit=True):
        review = self.instance
        review.headline = self.cleaned_data['headline']
        review.body = self.cleaned_data['body']
        review.rating = self.cleaned_data['rating']
        if commit:
            review.save()
        return review
