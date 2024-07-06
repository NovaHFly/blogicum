from datetime import timedelta

import pytest
from django.contrib.auth.base_user import AbstractBaseUser
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from blog.models import Category, Comment, Location, Post


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
def author(django_user_model) -> AbstractBaseUser:
    return django_user_model.objects.create(username='post_author')


@pytest.fixture
def author_client(author) -> Client:
    return _create_client(author)


@pytest.fixture
def location() -> Location:
    return Location.objects.create(name='Location')


@pytest.fixture
def category() -> Category:
    return Category.objects.create(
        title='Category title',
        slug='cat_slug',
        description='Description',
    )


@pytest.fixture
def post(author, location, category) -> Post:
    return Post.objects.create(
        title='Title',
        text='Text',
        pub_date=timezone.now(),
        author=author,
        location=location,
        category=category,
    )


@pytest.fixture
def comment(author, post) -> Comment:
    return Comment.objects.create(
        text='Comment text',
        author=author,
        post=post,
    )


@pytest.fixture
def index_url() -> str:
    return reverse('blog:index')


@pytest.fixture
def rules_url() -> str:
    return reverse('pages:rules')


@pytest.fixture
def about_url() -> str:
    return reverse('pages:about')


@pytest.fixture
def profile_url(author) -> str:
    return reverse('blog:profile', args=(author.username,))


@pytest.fixture
def profile_edit_url() -> str:
    return reverse('blog:edit_profile')


@pytest.fixture
def category_url(category) -> str:
    return reverse('blog:category_posts', args=(category.slug,))


@pytest.fixture
def post_create_url() -> str:
    return reverse('blog:create_post')


@pytest.fixture
def post_detail_url(post) -> str:
    return reverse('blog:post_detail', args=(post.id,))


@pytest.fixture
def post_edit_url(post) -> str:
    return reverse('blog:edit_post', args=(post.id,))


@pytest.fixture
def post_delete_url(post) -> str:
    return reverse('blog:delete_post', args=(post.id,))


@pytest.fixture
def comment_add_url(post) -> str:
    return reverse('blog:add_comment', args=(post.id,))


@pytest.fixture
def comment_edit_url(post, comment) -> str:
    return reverse('blog:edit_comment', args=(post.id, comment.id))


@pytest.fixture
def comment_delete_url(post, comment) -> str:
    return reverse('blog:delete_comment', args=(post.id, comment.id))


# ^ Auth urls
@pytest.fixture
def signup_url() -> str:
    return reverse('registration')


@pytest.fixture
def logout_url() -> str:
    return reverse('logout')


@pytest.fixture
def login_url() -> str:
    return reverse('login')


# ^ Fixtures related to Unpublished posts


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
