import pytest

from django.urls import reverse
from django.test import Client
from library.models import Ticket, Review, UserFollows
from django.test import RequestFactory

from account.models import User
from library.forms import TicketCreationForm
from library.views import ticket_creation, review_creation


class TestLibrary:
    """
    """

    def setup(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()

    def test_urls_flow(self) -> None:
        response = self.client.get(reverse('library:flow'))
        assert response.status_code == 302

    def test_urls_ticket_creation(self) -> None:

        response = self.client.get(reverse('library:ticket_creation'))
        assert response.status_code == 302

    def test_urls_review_creation(self) -> None:

        response = self.client.get(reverse('library:review_creation'))
        assert response.status_code == 302
    
    def test_urls_review_creation(self) -> None:

        response = self.client.get(reverse('library:review_ticket'))
        assert response.status_code == 302

    # ############################################################## #
    # #######################  FIXTURES ############################ #

    @pytest.fixture
    def user_ticket(self, db) -> User:
        return User.objects.create_user(username='moi', password='mon_password_test')

    @pytest.fixture
    def other_user(self, db) -> User:
        return User.objects.create_user(username='lautre', password='password_autre_test')

    @pytest.fixture
    def one_ticket(self, db, user_ticket: User) -> Ticket:
        return Ticket.objects.create(title='Mon livre préféré', user=user_ticket)

    @pytest.fixture
    def user_ticket_follows_other_user(self, db, user_ticket: User, other_user: User) -> UserFollows:
        return UserFollows.objects.create(user=user_ticket, followed_user=other_user)

    # ############################################################## #
    # ###################  TESTS STR models ######################## #

    def test_str_tickets(self, one_ticket: Ticket) -> None:
        assert str(one_ticket) == 'Mon livre préféré - by moi'

    def test_str_review(self, other_user: User, one_ticket: Ticket) -> None:
        Review.objects.create(ticket=one_ticket, rating=3, headline='Bon livre', user=other_user)
        review = Review.objects.get(id=1)
        assert str(review) == 'Bon livre - by lautre - related to ticket Mon livre préféré'

    def test_str_userfollows(self, user_ticket_follows_other_user: UserFollows) -> None:
        assert str(user_ticket_follows_other_user) == 'MOI follows LAUTRE'

    # ############################################################## #
    # #####################  TESTS Tickets ######################### #

    def test_new_ticket_view(self, user_ticket: User) -> None:
        request = self.factory.get('/ticket')
        request.user = user_ticket
        response = ticket_creation(request)
        assert response.status_code == 200

    def test_ticket_creation(self, user_ticket: User) -> None:
        ticket_count = Ticket.objects.count()
        self.client.login(username='moi', password='mon_password_test')
        response = self.client.post(reverse('library:ticket_creation'),
                                    data={'title': 'new book',
                                          'description': 'quel beau livre',
                                          'user': user_ticket,
                                          'image': ''})
        assert response.status_code == 302
        assert Ticket.objects.count() == ticket_count + 1

    def test_ticket_creation_response_invalid(self, user_ticket: User) -> None:
        self.client.login(username='moi', password='mon_password_test')
        response = self.client.post(reverse('library:ticket_creation'),
                                    data={'title': '',
                                          'description': 'description',
                                          'user': user_ticket,
                                          'image': ''})
        assert response.content == b'Formulaire invalide'

    # ############################################################## #
    # #####################  TESTS Reviews ######################### #

    def test_new_review_view(self, user_ticket: User) -> None:
        request = self.factory.get('/review')
        request.user = user_ticket
        response = review_creation(request)
        assert response.status_code == 200

    def test_review_creation(self, user_ticket: User, one_ticket: Ticket) -> None:
        review_count = Review.objects.count()
        self.client.login(username='moi', password='mon_password_test')

        response = self.client.post(reverse('library:review_creation'),
                                    data={'title': 'new book',
                                          'description': 'quel beau livre',
                                          'user': user_ticket,
                                          'image': '',
                                          'headline': 'good book',
                                          'body': 'quel beau livre',
                                          'user': user_ticket,
                                          'rating': 4,
                                          'ticket': one_ticket})
        assert response.status_code == 302
        assert Review.objects.count() == review_count + 1

    def test_review_creation_invalid_response(self, user_ticket: User, one_ticket: Ticket) -> None:
        self.client.login(username='moi', password='mon_password_test')
        response = self.client.post(reverse('library:review_creation'),
                                    data={'title': '',
                                          'description': 'quel beau livre',
                                          'user': user_ticket,
                                          'image': '',
                                          'headline': 'good book',
                                          'body': 'quel beau livre',
                                          'user': user_ticket,
                                          'rating': 4,
                                          'ticket': one_ticket})
        assert response.content == b'Formulaire invalide'
