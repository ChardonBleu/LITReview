from itertools import chain
from django.http.response import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket
from .forms import TicketCreationForm


@login_required(login_url='/')
def flow(request) -> HttpResponse:
    """group all tickets and  review for flow.

    """
    tickets = Ticket.objects.get_users_viewable_tickets(request)
    reviews = Review.objects.get_users_viewable_reviews(request)

    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.datetime_created,
                   reverse=True)
    context = {'posts': posts}

    return render(request, 'library/flow.html', context)

@login_required(login_url='/')
def ticket_creation(request) -> HttpResponse:
    """group all tickets and  review for flow.
    """
    if request.method == "POST":
        form = TicketCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:flow')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        form = TicketCreationForm()

    return render(request, 'library/ticket.html', context={"form": form})
