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

        response = self.client.get(reverse('library:flow'))
        self.assertEqual(response.status_code, 302)
        print("page flow OK")
