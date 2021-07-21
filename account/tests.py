from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import User


# Create your tests here.
class UserViewTests(TestCase):
    """[summary]

    Arguments:
        TestCase {[type]} -- [description]
    """

    def setUp(self):
        """[summary]
        """
        self.current_user = User.objects.create(username='current_user_test', password='user_test')
        self.other_user = User.objects.create(username="other_user_test", password="other_user")
        self.client = Client()

    def test_urls(self):
        """[summary]
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("page acceuil OK")

        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        print("page inscription OK")

        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        print("page logout OK")

    def test_registration(self):
        response = self.client.post('/register/', {'username': 'toto', 'password': 'navet'})
        user_registered = User.objects.get(id=1)
        print(user_registered)
        self.assertEqual(response.status_code, 200)
