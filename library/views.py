from itertools import chain

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value

from .models import Review, Ticket, UserFollows


def get_users_viewable_reviews(request):
    """[summary]

    Returns:
        [list] -- liste de résultats de requêtes annotées
    """
    reviews = Review.objects.filter(user_id=request.id)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    own_tickets = Ticket.objects.filter(user_id=request.id)
    for ticket in own_tickets:
        reviews_to_own_ticket = Review.objects.filter(ticket_id=ticket.id)
        reviews_to_own_ticket = reviews_to_own_ticket.annotate(content_type=Value('REVIEW', CharField()))
        reviews = sorted(chain(reviews, reviews_to_own_ticket),
                         key=lambda post: post.datetime_created,
                         reverse=True)

    followed_users = UserFollows.objects.filter(user_id=request.id)
    for followed in followed_users:
        reviews_followed_users = Review.objects.filter(user_id=followed.followed_user.id)
        reviews_followed_users = reviews_followed_users.annotate(content_type=Value('REVIEW', CharField()))
        reviews = sorted(chain(reviews, reviews_followed_users),
                         key=lambda post: post.datetime_created,
                         reverse=True)

    return reviews


def get_users_viewable_tickets(request):
    """[summary]


    Returns:
        [type] -- [description]
    """
    tickets = Ticket.objects.filter(user_id=request.id)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    followed_users = UserFollows.objects.filter(user_id=request.id)
    for followed in followed_users:
        tickets_followed_users = Ticket.objects.filter(user_id=followed.followed_user.id)
        tickets_followed_users = tickets_followed_users.annotate(content_type=Value('TICKET', CharField()))
        tickets = sorted(chain(tickets, tickets_followed_users),
                         key=lambda post: post.datetime_created,
                         reverse=True)

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

    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.datetime_created,
                   reverse=True)
    context = {'posts': posts}

    return render(request, 'library/flow.html', context)
