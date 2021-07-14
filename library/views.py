from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


from .forms import CustomUserCreationForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


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
                return redirect('library:login')
            else:
                return HttpResponse("Formulaire invalide")
    else:
        form = CustomUserCreationForm()

    return render(request, 'library/register.html', context={"form": form})


@login_required(login_url='/')
def flow(request):
    """[summary]

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return render(request, 'library/flow.html', context={})
