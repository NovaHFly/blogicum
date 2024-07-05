from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture as lf


@pytest.fixture
def rules_url() -> str:
    return reverse('pages:rules')


@pytest.fixture
def about_url() -> str:
    return reverse('pages:about')


OK = HTTPStatus.OK


@pytest.mark.parametrize(
    'url',
    (
        lf('rules_url'),
        lf('about_url'),
    ),
)
def test_static_page_routes(client, url):
    """Test if static pages are available for anyone."""
    assert client.get(url).status_code == OK
