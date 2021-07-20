from itertools import chain
from django.http.response import HttpResponse
from django.db.models import CharField, Value

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket, UserFollows


@login_required(login_url='/')
def flow(request) -> HttpResponse:
    """group all tickets and  review for flow.

    """
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    followed_users = UserFollows.objects.filter(user=request.user)
    for followed in followed_users:
        tickets_followed_users = Ticket.objects.filter(user=followed.followed_user)
        tickets_followed_users = tickets_followed_users.annotate(content_type=Value('TICKET', CharField()))
        tickets = sorted(chain(tickets, tickets_followed_users),
                         key=lambda post: post.datetime_created,
                         reverse=True)

    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    own_tickets = Ticket.objects.filter(user=request.user)
    for ticket in own_tickets:
        reviews_to_own_ticket = Review.objects.filter(ticket=ticket)
        reviews_to_own_ticket = reviews_to_own_ticket.annotate(content_type=Value('REVIEW', CharField()))
        reviews = sorted(chain(reviews, reviews_to_own_ticket),
                         key=lambda post: post.datetime_created,
                         reverse=True)

    for followed in followed_users:
        reviews_followed_users = Review.objects.filter(user=followed.followed_user)
        reviews_followed_users = reviews_followed_users.annotate(content_type=Value('REVIEW', CharField()))
        if list(reviews_followed_users)[0] not in reviews:
            reviews = sorted(chain(reviews, reviews_followed_users),
                             key=lambda post: post.datetime_created,
                             reverse=True)

    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.datetime_created,
                   reverse=True)
    context = {'posts': posts}

    return render(request, 'library/flow.html', context)
