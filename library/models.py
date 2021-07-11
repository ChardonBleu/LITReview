from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Ticket(models.Model):
    """Describe a book or article wich can receive reviews.
    * Each ticket has a title which is the book or article title.
    * Each ticket has a description. It can describe the book and/or can
    request for information on this book.
    * Each ticket has been created by one user. If the user is deleted, the
    ticket is deleted.
    * Each ticket can have an image. It can be blank.
    * ticket creation date is automatically filled in.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """display the essentials of a ticket on one line

        Returns:
            [string] -- ticket title, creation date and related user id
        """
        return f"{self.title} - created on {self.time_created} - related to ticket id {self.user}"


class Review(models.Model):
    """Reviews for books or articles.
    * Each review is related to a Ticket describing a book or an article. If a
    the related ticket is deleted, the review is deleted.
    * Each review has a rating wich is an integer number between 0 and 5.
    * The headline can't be blank. Headline max length is 128.
    * The body can be blank. Body max length is 8192.
    * Each review is related tu a user. If the user is deleted, the review is
    deleted.
    * review creation date is automatically filled in.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """display the essentials of a review on one line

        Returns:
            [string] -- review title, creation date and related ticket id
        """

        return f"{self.headline} - created on {self.time_created} - related to ticket id {self.ticket}"


class User(AbstractUser):
    pass


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    """[summary]

    Arguments:
        models {[type]} -- [description]
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )
