from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url',
    (
        lf('signup_url'),
        lf('login_url'),
        lf('index_url'),
        lf('about_url'),
        lf('rules_url'),
        lf('category_url'),
        lf('post_detail_url'),
        lf('profile_url'),
    ),
)
def test_routes_anonymous(client, url):
    response = client.get(url)
    assert response.status_code == OK


@pytest.mark.parametrize(
    'url',
    (
        lf('profile_edit_url'),
        lf('post_create_url'),
    ),
)
def test_routes_logged_in(user_client, url):
    response = user_client.get(url)
    assert response.status_code == OK


@pytest.mark.parametrize(
    'url',
    (
        lf('post_edit_url'),
        lf('post_delete_url'),
        lf('comment_edit_url'),
        lf('comment_delete_url'),
    ),
)
def test_routes_author(author_client, url):
    response = author_client.get(url)
    assert response.status_code == OK


def test_unpublished_category(author_client, unpub_cat_url):
    response = author_client.get(unpub_cat_url)
    assert response.status_code == NOT_FOUND


@pytest.mark.parametrize(
    'param_client, status',
    (
        (lf('user_client'), NOT_FOUND),
        (lf('author_client'), OK),
    ),
)
@pytest.mark.parametrize(
    'url',
    (
        lf('unpublished_post_url'),
        lf('unpub_cat_post_url'),
        lf('delayed_post_url'),
    ),
)
def test_unpublished(param_client, url, status):
    response = param_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (
        lf('profile_edit_url'),
        lf('post_create_url'),
        lf('comment_add_url'),
    ),
)
def test_anonymous_redirects(client, url, login_url):
    response = client.get(url)
    assertRedirects(response, f'{login_url}?next={url}')


@pytest.mark.parametrize(
    'url',
    (
        lf('post_edit_url'),
        lf('post_delete_url'),
        lf('comment_edit_url'),
        lf('comment_delete_url'),
    ),
)
def test_user_redirects(user_client, url, post_detail_url):
    response = user_client.get(url)
    assertRedirects(response, post_detail_url)
