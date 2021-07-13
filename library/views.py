from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm


def register(request):
    """
    Arguments:
        request {[type]} -- [description]
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('library:log_in')
            else:
                return HttpResponse("Formulaire invalide")
    else:
        form = CustomUserCreationForm()

    return render(request, 'library/register.html', context={"form": form})


@login_required()
def flux(request):
    """[summary]

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return render(request, 'library/flux.html', context={})
