from account.models import User
from django import forms
from django.forms.widgets import RadioSelect
from .models import Ticket, Review, UserFollows


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
        widgets = {
            'rating': RadioSelect(attrs={
                'class': ' form-check form-check-inline'}),
        }


class FollowedForm(forms.ModelForm):
    """used to add followers subscriptions
    exclusion of authenticated user un form list

    """
    class Meta:
        model = UserFollows
        fields = ['followed_user']

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('user')
        super(FollowedForm, self).__init__(*args, **kwargs)
        self.fields['followed_user'] = forms.ModelChoiceField(
            queryset=User.objects.all().exclude(username=username))
