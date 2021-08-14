from itertools import chain
from typing import Dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse, reverse_lazy
from django.utils.functional import lazy

from django.views.generic.edit import CreateView

from .models import Review, Ticket, UserFollows
from .forms import TicketForm, ReviewForm


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
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('library:flow')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        form = TicketForm()
    return render(request, 'library/ticket.html', context={"form": form})

@login_required(login_url='/')
def review_creation(request) -> HttpResponse:

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
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
        review_form = ReviewForm()
        ticket_form = TicketForm()
    context = {"review_form": review_form, "ticket_form": ticket_form}
    return render(request, 'library/review.html', context=context)

@login_required(login_url='/')
def review_for_ticket(request, ticket_id) -> HttpResponse:
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
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
        review_form = ReviewForm()
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
            <a href='../../../posts/'>Retour</a>")
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
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
        form = TicketForm(data)
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
    if review.user != request.user:
        return HttpResponse("Vous ne pouvez modifier une critique dont vous n'êtes pas l'auteur.<br>\
            <a href='../../../posts/'>Retour</a>")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
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
        form = ReviewForm(data)
    context = {"form": form, "review": review}
    return render(request, 'library/modify_review.html', context=context)


class FollowingView(LoginRequiredMixin, CreateView):
    model = UserFollows
    fields = ['followed_user']
    success_url = reverse_lazy('library: following')

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        user_subscriptions = UserFollows.objects.get_users_subscriptions(self.request)
        user_followers = UserFollows.objects.get_users_followers(self.request)
        context['subscriptions'] = user_subscriptions
        context['followers'] = user_followers
        return context

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """
        If the form is valid, redirect to the supplied URL
        """
        context = super().get_context_data(**kwargs)
        user_subscriptions = UserFollows.objects.get_users_subscriptions(self.request)
        user_followers = UserFollows.objects.get_users_followers(self.request)
        context['subscriptions'] = user_subscriptions
        context['followers'] = user_followers
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        if model_instance.followed_user == self.request.user:
            return HttpResponse("Vous ne pouvez pas vous suivre vous même.<br> <a href='../../../following/'>Retour</a>")
        else:
            model_instance.save()
        return render(self.request, 'library/userfollows_form.html', context=context)
