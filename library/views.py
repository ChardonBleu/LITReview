from itertools import chain
from django.http.response import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket
from .forms import TicketCreationForm, ReviewCreationForm


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
        form = TicketCreationForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('library:flow')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        form = TicketCreationForm()
    return render(request, 'library/ticket.html', context={"form": form})

@login_required(login_url='/')
def review_creation(request) -> HttpResponse:

    if request.method == "POST":
        ticket_form = TicketCreationForm(request.POST, request.FILES)
        review_form = ReviewCreationForm(request.POST)
        if review_form.is_valid() and ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('library:flow')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        review_form = ReviewCreationForm()
        ticket_form = TicketCreationForm()
    context = {"review_form": review_form, "ticket_form": ticket_form}

    return render(request, 'library/review.html', context=context)
