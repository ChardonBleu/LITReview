from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    """
    Custom login class using a custom authentication form.
    """
    form_class = CustomAuthenticationForm


def register(request) -> HttpResponse:
    """
    This view implements a form for registration.
    After registration returns to the login page.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('account:login')
            else:
                return HttpResponse("Formulaire invalide")
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/register.html', context={"form": form})
