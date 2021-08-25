import pytest
import uuid
from django.urls import reverse
from django.test import Client

from .models import User
from .forms import CustomUserCreationForm


@pytest.fixture
def current_user(db) -> User:
    return User.objects.create_user(username='azalae', password='choucroute')


@pytest.fixture
def client(db) -> Client:
    return Client()


@pytest.fixture
def connect_client(client: Client, current_user: User) -> Client:
    client.login(username='azalae', password='choucroute')
    return client, current_user


@pytest.fixture
def test_password() -> str:
    return 'test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(db, user=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
            return client, user
    return make_auto_login

# ################################################################# #
# ############################ TEST URLS ########################## #


def test_urls(client: Client) -> None:
    """[summary]
    """
    response = client.get('/')
    assert response.status_code == 200

    response = client.get(reverse('account:register'))
    assert response.status_code == 200

    response = client.get(reverse('account:logout'))
    assert response.status_code == 302

# ################################################################# #
# ######################### TEST connexion ############# ########## #


def test_unauthorized_user_on_admin(client: Client) -> None:
    response = client.get('/admin/')
    assert response.status_code == 302


def test_superuser_on_admin(admin_client) -> None:
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_auth_view(db, auto_login_user: Client) -> None:
    client, user = auto_login_user(db)
    url = reverse('library:flow')
    response = client.get(url)
    assert response.status_code == 200

# ################################################################# #
# ####################### TEST registration ####################### #


def test_registration(db, client: Client) -> None:
    user_count = User.objects.count()
    response = client.post(reverse('account:register'), data={
        'username': 'azalae',
        'password1': 'choucroute',
        'password2': 'choucroute'})
    assert response.status_code == 302
    assert User.objects.count() == user_count + 1


def test_invalid_form(db) -> None:
    form_data = {
        'username': 'azalae',
        'password1': 'choucroute',
        'password2': ' '}
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()


def test_response_invalid(client: Client) -> None:
    response = client.post(reverse('account:register'), data={
        'username': 'azalae',
        'password1': 'choucroute',
        'password2': ' '})
    assert response.content == b'Formulaire invalide'
