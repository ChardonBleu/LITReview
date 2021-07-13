from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.views import LoginView

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


class CustomAuthenticationForm(AuthenticationForm):
    """

    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'placeholder': 'Utilisateur'}),
                             label=(""))
    password = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Mot de passe'})
    )


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
