from django.test import TestCase
from django.urls import reverse
from django.test import Client
from account.models import User


# Create your tests here.
class UserViewTests(TestCase):
    """[summary]

    Arguments:
        TestCase {[type]} -- [description]
    """

    def setUp(self):
        """[summary]
        """
        self.client = Client()

    def test_urls(self):
        """[summary]
        """
        response = self.client.get(reverse('library:flow'))
        self.assertEqual(response.status_code, 302)
        print("page flow OK")
