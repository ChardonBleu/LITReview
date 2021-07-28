import pytest
from django.urls import reverse
from django.test import Client

from django.http.response import HttpResponse

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

    def test_registration(self):
        pass
