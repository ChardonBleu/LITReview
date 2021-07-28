import pytest
from django.urls import reverse
from django.test import Client


from .models import User


# Create your tests here.
class TestUserView:
    """[summary]

    Arguments:
        TestCase {[type]} -- [description]
    """

    def setup(self):
        """[summary]
        """
        self.client = Client()

    def test_urls(self):
        """[summary]
        """
        response = self.client.get('/')
        assert response.status_code == 200

        response = self.client.get(reverse('account:register'))
        assert response.status_code == 200

        response = self.client.get(reverse('account:logout'))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_user_create(self):
        User.objects.create_user('toto', 'zeropluszero')
        assert User.objects.count() == 1
    
    def test_registration(self):
        pass
