from itertools import chain
from django.db.models.query import InstanceCheckMeta
from django.http.response import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket
from .forms import TicketCreationForm, ReviewCreationForm, TicketUpdateForm, ReviewUpdateForm


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
            ticket.related_review = True
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

@login_required(login_url='/')
def review_for_ticket(request, ticket_id) -> HttpResponse:
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        review_form = ReviewCreationForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            ticket.related_review = True
            review.ticket = ticket
            review.save()
            return redirect('library:flow')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        review_form = ReviewCreationForm()
    context = {"review_form": review_form, "ticket": ticket}
    return render(request, 'library/review_ticket.html', context=context)

@login_required(login_url='/')
def posts(request) -> HttpResponse:
    tickets = Ticket.objects.get_own_tickets(request)
    reviews = Review.objects.get_own_reviews(request)

    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.datetime_created,
                   reverse=True)
    context = {'posts': posts}

    return render(request, 'library/posts.html', context)

@login_required(login_url='/')
def post_modification_ticket(request, ticket_id) -> HttpResponse:
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        return HttpResponse("Vous ne pouvez modifier un ticket dont vous n'êtes pas l'auteur.<br>\
            <a href='{% url 'library:post' %}'>Retour</a>")
    if request.method == "POST":
        form = TicketUpdateForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('library:posts')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        data = {
            'title': ticket.title,
            'description': ticket.description,
            'image': ticket.image
        }
        form = TicketUpdateForm(data)
    context = {"form": form, "ticket": ticket}
    return render(request, 'library/modify_ticket.html', context=context)

@login_required(login_url='/')
def ticket_deletion(request, ticket_id) -> HttpResponse:
    Ticket.objects.filter(id=ticket_id).delete()
    return redirect('library:posts')

@login_required(login_url='/')
def review_deletion(request, review_id) -> HttpResponse:
    Review.objects.filter(id=review_id).delete()
    return redirect('library:posts')

@login_required(login_url='/')
def post_modification_review(request, review_id) -> HttpResponse:
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        form = ReviewUpdateForm(request.POST, instance=review)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('library:posts')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        data = {
            'headline': review.headline,
            'body': review.body,
            'rating': review.rating
        }
        form = ReviewUpdateForm(data)
    context = {"form": form, "review": review}
    return render(request, 'library/modify_review.html', context=context)
