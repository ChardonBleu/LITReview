from itertools import chain

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import CharField, Value

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Review, Ticket


class CustomLoginView(LoginView):
    """
    Custom login class using a custom authentication form.
    """
    form_class = CustomAuthenticationForm


def register(request):
    """
    This view implements a form for registration.
    After registration returns to the login page.

    return: envoie le formulaire sur la page d'enregistrement.
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


def get_users_viewable_reviews(request):
    reviews = Review.objects.filter(user_id=request.id)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    own_tickets = Ticket.objects.filter(user_id=request.id)
    for ticket in own_tickets:
        reviews_to_own_ticket = Review.objects.filter(ticket_id=ticket.id)
        reviews_to_own_ticket = reviews_to_own_ticket.annotate(content_type=Value('REVIEW', CharField()))
        reviews = sorted(chain(reviews, reviews_to_own_ticket),
                         key=lambda post: post.time_created,
                         reverse=True)
    return reviews


def get_users_viewable_tickets(request):
    tickets = Ticket.objects.filter(user_id=request.id)
    return tickets


@login_required(login_url='/')
def flow(request):
    """[summary]

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    reviews = get_users_viewable_reviews(request.user)

    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created,
                   reverse=True)
    context = {'posts': posts}

    return render(request, 'library/flow.html', context)
