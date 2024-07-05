from datetime import timedelta
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_lazyfixture import lazy_fixture as lf

from blog.models import Category, Post


@pytest.fixture
def unpublished_category() -> Category:
    return Category.objects.create(
        title='Unpublished category',
        slug='unpub',
        description='Unpublished description',
        is_published=False,
    )


@pytest.fixture
def unpublished_post(author, location, category) -> Post:
    return Post.objects.create(
        title='Unpublished title',
        text='This post was unpublished',
        pub_date=timezone.now(),
        author=author,
        location=location,
        category=category,
        is_published=False,
    )


@pytest.fixture
def delayed_post(author, location, category) -> Post:
    return Post.objects.create(
        title='Delayed title',
        text='This post was delayed',
        pub_date=timezone.now() + timedelta(days=3),
        author=author,
        location=location,
        category=category,
    )


@pytest.fixture
def unpub_category_post(
    author,
    location,
    unpublished_category,
) -> Post:
    return Post.objects.create(
        title='Post in unpublished category',
        text="This post's category was unpublished",
        pub_date=timezone.now(),
        author=author,
        location=location,
        category=unpublished_category,
    )


@pytest.fixture
def unpub_category_url(unpublished_category) -> str:
    return reverse('blog:category_posts', args=(unpublished_category.slug,))


@pytest.fixture
def unpub_post_url(unpublished_post) -> str:
    return reverse('blog:post_detail', args=(unpublished_post.id,))


@pytest.fixture
def unpub_category_post_url(unpub_category_post) -> str:
    return reverse(
        'blog:post_detail',
        args=(unpub_category_post.id,),
    )


@pytest.fixture
def delayed_post_url(delayed_post) -> str:
    return reverse('blog:post_detail', args=(delayed_post.id,))


OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'param_client, status_code',
    (
        (lf('user_client'), NOT_FOUND),
        (lf('author_client'), OK),
    ),
)
@pytest.mark.parametrize(
    'url',
    (
        lf('unpub_post_url'),
        lf('unpub_category_post_url'),
        lf('delayed_post_url'),
    ),
)
def test_post_routes(param_client, url, status_code):
    assert param_client.get(url).status_code == status_code


def test_unpub_category_route(author_client, unpub_category_url):
    assert author_client.get(unpub_category_url).status_code == NOT_FOUND
