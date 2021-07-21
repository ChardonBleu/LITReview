from itertools import chain
from django.http.response import HttpResponse
from django.db.models import CharField, Value
from django.db.models import Q

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket, UserFollows


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
