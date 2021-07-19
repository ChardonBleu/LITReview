from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    personalized registration form with placeholders instead of labels
    """
    username = forms.CharField(
        label=(""),
        widget=forms.TextInput(attrs={'placeholder': 'Utilisateur'}),
    )
    password1 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Mot de passe'}),
    )
    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Confirmer mot de passe'}),
    )

    class Meta(UserCreationForm.Meta):
        """
        use of the personalized user for the creation of
        new users
        """
        model = User


class CustomAuthenticationForm(AuthenticationForm):
    """
    personalized authentication form with placeholders instead of labels
    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'placeholder': 'Utilisateur'}),
                             label=(""))
    password = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Mot de passe'})
    )
