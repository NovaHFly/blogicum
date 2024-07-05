import pytest
from django.contrib.auth.base_user import AbstractBaseUser
from django.test import Client
from django.urls import reverse


def _create_client(user: AbstractBaseUser) -> Client:
    client = Client()
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture
def user(django_user_model) -> AbstractBaseUser:
    return django_user_model.objects.create(username='user')


@pytest.fixture
def user_client(user) -> Client:
    return _create_client(user)


@pytest.fixture
def login_url() -> str:
    return reverse('login')
