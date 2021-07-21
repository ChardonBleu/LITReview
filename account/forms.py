from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    personalized registration form with placeholders instead of labels
    """

    class Meta(UserCreationForm.Meta):
        """
        use of the personalized user for the creation of
        new users
        """
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['username'].help_text = ""
        self.fields['username'].widget.attrs.update({'autofocus': True,
                                                     'placeholder': 'Utilisateur'})

        self.fields['password1'].label = ""
        self.fields['password1'].help_text = ""
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password',
                                                      'placeholder': 'Mot de passe'})

        self.fields['password2'].label = ""
        self.fields['password2'].help_text = ""
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password',
                                                     'placeholder': 'Confirmer mot de passe'})


class CustomAuthenticationForm(AuthenticationForm):
    """
    personalized authentication form with placeholders instead of labels
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['username'].help_text = ""
        self.fields['username'].widget.attrs.update({'autofocus': True,
                                                     'placeholder': 'Utilisateur'})

        self.fields['password'].label = ""
        self.fields['password'].help_text = ""
        self.fields['password'].widget.attrs.update({'autocomplete': 'new-password',
                                                     'placeholder': 'Mot de passe'})
