from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def log_in(request):
    """
    Arguments:
        request {[type]} -- [description]
    """

    return render(request, 'library/log_in.html', context={})


def register(request):
    """
    Arguments:
        request {[type]} -- [description]
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:log_in')
    else:
        form = CustomUserCreationForm()

    return render(request, 'library/register.html', context={"form": form})
