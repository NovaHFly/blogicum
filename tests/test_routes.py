from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url, param_client, status_code',
    (
        (lf('index_url'), lf('client'), OK),
        (lf('category_url'), lf('client'), OK),
        (lf('post_detail_url'), lf('client'), OK),
        (lf('profile_url'), lf('client'), OK),
        (lf('profile_edit_url'), lf('user_client'), OK),
        (lf('post_create_url'), lf('user_client'), OK),
        (lf('post_edit_url'), lf('author_client'), OK),
        (lf('post_delete_url'), lf('author_client'), OK),
        (lf('comment_edit_url'), lf('author_client'), OK),
        (lf('comment_delete_url'), lf('author_client'), OK),
        (lf('unpub_post_url'), lf('user_client'), NOT_FOUND),
        (lf('unpub_category_post_url'), lf('user_client'), NOT_FOUND),
        (lf('delayed_post_url'), lf('user_client'), NOT_FOUND),
        (lf('unpub_post_url'), lf('author_client'), OK),
        (lf('unpub_category_post_url'), lf('author_client'), OK),
        (lf('delayed_post_url'), lf('author_client'), OK),
        (lf('unpub_category_url'), lf('author_client'), NOT_FOUND),
        (lf('signup_url'), lf('client'), OK),
        (lf('login_url'), lf('client'), OK),
        (lf('rules_url'), lf('client'), OK),
        (lf('about_url'), lf('client'), OK),
    ),
)
def test_page_availability(url, param_client, status_code):
    assert param_client.get(url).status_code == status_code


def test_logout_route(user_client, logout_url):
    assert user_client.post(logout_url).status_code == OK


@pytest.mark.parametrize(
    'url',
    (
        lf('profile_edit_url'),
        lf('post_create_url'),
        lf('comment_add_url'),
    ),
)
def test_redirects_to_login(client, url, login_url):
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
def test_redirects_to_post_detail(user_client, url, post_detail_url):
    response = user_client.get(url)
    assertRedirects(response, post_detail_url)
