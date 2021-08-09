from django.urls.base import reverse_lazy
import pytest

from django.urls import reverse
from django.test import Client
from library.models import Ticket, Review, UserFollows
from django.test import RequestFactory

from account.models import User
from library.views import post_modification_ticket, ticket_creation, review_creation, review_for_ticket, posts
from library.views import ticket_deletion, review_deletion, post_modification_review


# ############################################################## #
# #######################  FIXTURES ############################ #


@pytest.fixture
def current_user(db) -> User:
    return User.objects.create_user(username='moi', password='mon_password_test')

@pytest.fixture
def client(db) -> Client:
    return Client()

@pytest.fixture
def factory(db) -> RequestFactory:
    return RequestFactory()

@pytest.fixture
def connect_client(client: Client, current_user: User) -> Client:
    client.login(username='moi', password='mon_password_test')
    return client, current_user

@pytest.fixture
def other_user(db) -> User:
    return User.objects.create_user(username='lautre', password='password_autre_test')

@pytest.fixture
def one_ticket(db, current_user: User) -> Ticket:
    return Ticket.objects.create(title='Mon livre préféré', user=current_user)

@pytest.fixture
def other_ticket(db, other_user: User) -> Ticket:
    return Ticket.objects.create(title='Mon livre préféré', user=other_user)

@pytest.fixture
def one_review(db, current_user: User, one_ticket: Ticket) -> Review:
    return Review.objects.create(headline='Très bon livre', user=current_user, rating=5, ticket=one_ticket)

@pytest.fixture
def other_review(db, other_user: User, other_ticket: Ticket) -> Review:
    return Review.objects.create(headline='Très bon livre', user=other_user, rating=5, ticket=other_ticket)

@pytest.fixture
def user_follows_other_user(db, current_user: User, other_user: User) -> UserFollows:
    return UserFollows.objects.create(user=current_user, followed_user=other_user)

# ############################################################## #
# ###################  TESTS STR models ######################## #

def test_str_tickets(one_ticket: Ticket) -> None:
    assert str(one_ticket) == 'Mon livre préféré - by moi'

def test_str_review(other_user: User, one_ticket: Ticket) -> None:
    Review.objects.create(ticket=one_ticket, rating=3, headline='Bon livre', user=other_user)
    review = Review.objects.get(id=1)
    assert str(review) == 'Bon livre - by lautre - related to ticket Mon livre préféré'

def test_str_userfollows(user_follows_other_user: UserFollows) -> None:
    assert str(user_follows_other_user) == 'MOI follows LAUTRE'

# ############################################################## #
# #####   ##############  TESTS url #####    ################### #


def test_urls(connect_client: Client, client: Client) -> None:
    """[summary]
    """
    connected_client, connected_user = connect_client
    response = connected_client.get('/')
    assert response.status_code == 200

    response = client.get(reverse('account:register'))
    assert response.status_code == 200

    response = connected_client.get(reverse('account:logout'))
    assert response.status_code == 302


# ############################################################## #
# #################  TESTS Tickets creation #################### #

def test_new_ticket_view(factory: RequestFactory, connect_client: Client) -> None:
    request = factory.get('/ticket')
    connected_client, connected_user = connect_client
    request.user = connected_user
    response = ticket_creation(request)
    assert response.status_code == 200

def test_ticket_creation(connect_client) -> None:
    connected_client, connected_user = connect_client
    ticket_count = Ticket.objects.count()
    response = connected_client.post(reverse('library:ticket_creation'),
                                     data={'title': 'new book',
                                           'description': 'quel beau livre',
                                           'user': connected_user,
                                           'image': ''})
    assert response.status_code == 302
    assert Ticket.objects.count() == ticket_count + 1

def test_ticket_creation_response_invalid(connect_client: Client) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:ticket_creation'),
                                     data={'title': '',
                                           'description': 'description',
                                           'user': connected_user,
                                           'image': ''})
    assert response.content == b'Formulaire invalide'

# ############################################################## #
# ##################  TESTS Reviews creation ################### #

def test_new_review_view(factory: RequestFactory, connect_client: Client) -> None:
    request = factory.get('/review')
    connected_client, connected_user = connect_client
    request.user = connected_user
    response = review_creation(request)
    assert response.status_code == 200

def test_review_creation(connect_client: Client, one_ticket: Ticket) -> None:
    review_count = Review.objects.count()
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:review_creation'),
                                     data={'title': 'new book',
                                           'description': 'quel beau livre',
                                           'user': connected_user,
                                           'image': '',
                                           'headline': 'good book',
                                           'body': 'quel beau livre',
                                           'user': connected_user,
                                           'rating': 4,
                                           'ticket': one_ticket})
    assert response.status_code == 302
    assert Review.objects.count() == review_count + 1

def test_review_creation_invalid_response(connect_client: Client, one_ticket: Ticket) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:review_creation'),
                                     data={'title': '',
                                           'description': 'quel beau livre',
                                           'user': connected_user,
                                           'image': '',
                                           'headline': 'good book',
                                           'body': 'quel beau livre',
                                           'user': connected_user,
                                           'rating': 4,
                                           'ticket': one_ticket})
    assert response.content == b'Formulaire invalide'

# ############################################################## #
# ############  TESTS Reviews for existing ticket ############## #

def test_review_for_ticket_view(factory: RequestFactory, connect_client: Client, one_ticket: Ticket) -> None:
    request = factory.get('/review_ticket/1/')
    connected_client, connected_user = connect_client
    request.user = connected_user
    request.ticket = one_ticket
    response = review_for_ticket(request, ticket_id=1)
    assert response.status_code == 200

def test_review_for_ticket_creation(connect_client: Client, one_ticket: Ticket) -> None:
    review_count = Review.objects.count()
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:review_ticket', args=[1]),
                                     data={'headline': 'good book',
                                           'body': 'quel beau livre',
                                           'user': connected_user,
                                           'rating': 4,
                                           'ticket': one_ticket})
    assert response.status_code == 302
    assert Review.objects.count() == review_count + 1

def test_review_for_ticket_invalid_response(connect_client: Client, one_ticket: Ticket) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:review_ticket', args=[1]),
                                     data={'headline': '',
                                           'body': 'quel beau livre',
                                           'user': connected_user,
                                           'rating': 4,
                                           'ticket': one_ticket})
    assert response.content == b'Formulaire invalide'

# ############################################################## #
# #######################  TESTS Posts ######################### #

def test_posts_view(factory: RequestFactory, connect_client: Client) -> None:
    request = factory.get('/posts/')
    connected_client, connected_user = connect_client
    request.user = connected_user
    response = posts(request)
    assert response.status_code == 200

def test_modify_ticket_view(factory: RequestFactory, connect_client: Client, one_ticket: Ticket) -> None:
    request = factory.get('/modify_ticket/1/')
    connected_client, connected_user = connect_client
    request.user = connected_user
    request.ticket = one_ticket
    response = post_modification_ticket(request, ticket_id=1)
    assert response.status_code == 200

def test_ticket_update(connect_client: Client, one_ticket: Ticket) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_ticket', args=[1]),
                                     data={'title': 'new book update',
                                           'description': 'quel beau livre',
                                           'image': 'logo.jpg'})
    assert response.status_code == 302

def test_ticket_update_unauthorized(connect_client: Client, other_ticket: Ticket) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_ticket', args=[1]),
                                     data={'title': 'new book update',
                                           'description': 'quel beau livre',
                                           'image': 'logo.jpg'})
    assert response.content == b"Vous ne pouvez modifier un ticket dont vous n'\xc3\xaates pas l'auteur.<br>            <a href='../../../posts/'>Retour</a>"

def test_ticket_update_response_invalid(connect_client: Client, one_ticket: Ticket) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_ticket', args=[1]),
                                     data={'title': '',
                                           'description': 'description',
                                           'image': ''})
    assert response.content == b'Formulaire invalide'

def test_delete_ticket_view(factory: RequestFactory, connect_client: Client) -> None:
    request = factory.get('TICKET/1/delete/')
    connected_client, connected_user = connect_client
    request.user = connected_user
    response = ticket_deletion(request, ticket_id=1)
    assert response.status_code == 302

def test_deldete_review_view(factory: RequestFactory, connect_client: Client) -> None:
    request = factory.get('REVIEW/1/delete')
    connected_client, connected_user = connect_client
    request.user = connected_user
    response = review_deletion(request, review_id=1)
    assert response.status_code == 302

def test_modify_review_view(factory: RequestFactory, connect_client: Client, one_review: Review) -> None:
    request = factory.get('/modify_review/1/')
    connected_client, connected_user = connect_client
    request.user = connected_user
    request.review = one_review
    response = post_modification_review(request, review_id=1)
    assert response.status_code == 200

def test_review_update(connect_client: Client, one_review: Review) -> None:
    review_before = Review.objects.get(id=1)
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_review', args=[1]),
                                     data={'headline': 'Trés trés bon livre',
                                           'body': '',
                                           'rating': '3'})
    review_after = Review.objects.get(id=1)
    assert response.status_code == 302
    assert review_before.headline != review_after.headline

def test_review_update_unauthorized(connect_client: Client, other_review: Review) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_review', args=[1]),
                                     data={'title': 'new book update',
                                           'description': 'quel beau livre',
                                           'image': 'logo.jpg'})
    assert response.content == b"Vous ne pouvez modifier une critique dont vous n'\xc3\xaates pas l'auteur.<br>            <a href='../../../posts/'>Retour</a>"

def test_review_update_response_invalid(connect_client: Client, one_review: Review) -> None:
    connected_client, connected_user = connect_client
    response = connected_client.post(reverse('library:modify_review', args=[1]),
                                     data={'headline': '',
                                           'body': 'description',
                                           'rating': '3'})
    assert response.content == b'Formulaire invalide'

# ######################################################################## #
# #######################  TESTS Following users ######################### #
