
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import CharField, Value
from itertools import chain

from django.db import models


class TicketManager(models.Manager):
    def get_users_viewable_tickets(self, request):
        """Select tickets for the flow page

        Returns:
            [iterable object] -- regroup all query results in one single list
        """
        tickets_user = self.filter(user=request.user)
        tickets_user = tickets_user.annotate(content_type=Value('TICKET', CharField()))

        tickets_followed_user = self.filter(user__followed_by__user=request.user)
        tickets_followed_user = tickets_followed_user.annotate(content_type=Value('TICKET', CharField()))
        tickets = sorted(chain(tickets_user, tickets_followed_user),
                         key=lambda post: post.datetime_created,
                         reverse=True)
        return tickets

    def get_own_tickets(self, request):
        """Select tickets for the posts page

        Returns:
            [iterable object] -- regroup all query results in one single list
        """
        tickets_user = self.filter(user=request.user)
        tickets_user = tickets_user.annotate(content_type=Value('TICKET', CharField()))

        return tickets_user


class Ticket(models.Model):
    """Describe a book or article wich can receive reviews.
    """

    title = models.CharField(
        max_length=128,
        help_text=_("Each ticket has a title wich is the book title and author"))
    description = models.TextField(
        max_length=2048,
        blank=True,
        help_text=_("Each ticket has a description.\
            It can describe the book and-or can request for information\
            on this book."))
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_("Each ticket has been created by one user.\
            If the user is deleted, the ticket is deleted."))
    image = models.ImageField(
        null=True,
        blank=True,
        help_text=_("Each ticket can have an image. It can be blank."),
        upload_to='library')
    datetime_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("ticket creation date is automatically filled in."))

    related_review = models.BooleanField(
        default=False,
        help_text="True if at least one review exists for this ticket")

    objects = TicketManager()

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self) -> str:
        """display the essentials of a ticket on one line

        Returns:
            [string] -- ticket title, creation date and related user id
        """
        return f"{self.title} - by {self.user}"


class ReviewManager(models.Manager):
    def get_users_viewable_reviews(self, request):
        """Select reviews for the flow page

        Returns:
            [iterable object] -- regroup all query results in one single list
        """
        reviews_user = Review.objects.filter(user=request.user)
        reviews_user = reviews_user.annotate(content_type=Value('REVIEW', CharField()))

        reviews_followed_user = Review.objects.filter(user__followed_by__user=request.user)
        reviews_followed_user = reviews_followed_user.annotate(content_type=Value('REVIEW', CharField()))
        reviews = sorted(chain(reviews_user, reviews_followed_user),
                         key=lambda post: post.datetime_created,
                         reverse=True)
        return reviews

    def get_own_reviews(self, request):
        """Select reviews for the flow page

        Returns:
            [iterable object] -- regroup all query results in one single list
        """
        reviews_user = Review.objects.filter(user=request.user)
        reviews_user = reviews_user.annotate(content_type=Value('REVIEW', CharField()))

        return reviews_user


class Review(models.Model):
    """Reviews for books or articles.
    * The body can be blank. Body max length is 8192.
    * Each review is related tu a user. If the user is deleted, the review is
    deleted.
    * review creation date is automatically filled in.
    """

    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        help_text=_("Each review is related to a Ticket describing a book or an article.\
            If a the related ticket is deleted, the review is deleted."),
        related_name='ticket')
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Each review has a rating wich is an integer number between 0 and 5.")
    )
    headline = models.CharField(
        max_length=128,
        help_text=_("The headline can't be blank. Headline max length is 128."))
    body = models.CharField(
        max_length=8192,
        blank=True,
        help_text=_("The body can be blank. Body max length is 8192."))
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_(""),
        related_name='user')
    datetime_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Each review is related tu a user. If the user is deleted,\
            the review is deleted."))

    objects = ReviewManager()

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self) -> str:
        """display the essentials of a review on one line

        Returns:
            [string] -- review title, creation date and related ticket id
        """

        return f"{self.headline} - by {self.user} - related to ticket {self.ticket.title}"


class UserFollows(models.Model):
    """Is used to memorize the users followed by a user
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        help_text=_(""))
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by',
        help_text=_(""))

    class Meta:
        """ Ensures we don't get multiple UserFollows instances
            for unique user-user_followed pairs
        """
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self) -> str:
        """display the essentials of user following and followers on one line

        Returns:
            [string] -- user1 follows user2
        """
        return f"{self.user.username.upper()} follows {self.followed_user.username.upper()}"
