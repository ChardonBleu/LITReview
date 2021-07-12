from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
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
        model = User
