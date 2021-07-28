import pytest
import uuid
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
    def test_unauthorized_user_on_admin(self):
        response = self.client.get('/admin/')
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_superuser_on_admin(self, admin_client):
        response = admin_client.get('/admin/')
        assert response.status_code == 200

    @pytest.fixture
    def test_password(self):
        return 'test-pass'

    @pytest.fixture
    def create_user(self, db, django_user_model, test_password):
        def make_user(**kwargs):
            kwargs['password'] = test_password
            if 'username' not in kwargs:
                kwargs['username'] = str(uuid.uuid4())
            return django_user_model.objects.create_user(**kwargs)
        return make_user

    @pytest.fixture
    def auto_login_user(self, db, client, create_user, test_password):
        def make_auto_login(user=None):
            if user is None:
                user = create_user()
            client.login(username=user.username, password=test_password)
            return client, user
        return make_auto_login

    @pytest.mark.django_db
    def test_auth_view(self, auto_login_user):
        client, user = auto_login_user()
        url = reverse('library:flow')
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_registration(self):
        User.objects.create_user('toto', 'zeropluszero')
        assert User.objects.count() == 1