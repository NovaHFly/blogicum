from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture as lf


@pytest.fixture
def signup_url() -> str:
    return reverse('registration')


@pytest.fixture
def logout_url() -> str:
    return reverse('logout')


OK = HTTPStatus.OK


@pytest.mark.parametrize(
    'url',
    (
        lf('signup_url'),
        lf('login_url'),
    ),
)
def test_auth_routes(client, url):
    assert client.get(url).status_code == OK


def test_logout_route(user_client, logout_url):
    assert user_client.post(logout_url).status_code == OK
