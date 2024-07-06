from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from blog.models import Comment, Post

User = get_user_model()

DAY_DIFF = 5


@pytest.fixture
def post_form_data(other_location, other_category) -> dict:
    return {
        'title': 'New title',
        'text': 'New text',
        'pub_date': timezone.now() - timedelta(days=DAY_DIFF),
        'category': other_category.id,
        'location': other_location.id,
        'image': '',
    }


@pytest.fixture
def comment_form_data(post) -> dict:
    return {'text': 'New comment text'}


@pytest.fixture
def profile_form_data() -> dict:
    return {
        'username': 'new_username',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'new_email@example.com',
    }


def test_anonymous_cant_edit_profile(
    client, profile_form_data, profile_edit_url
):
    client.post(profile_edit_url, data=profile_form_data)

    # Check if no user with username from form data was created/edited
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username=profile_form_data['username'])


def test_user_can_edit_profile(
    user_client,
    profile_form_data,
    profile_edit_url,
):
    response = user_client.post(profile_edit_url, data=profile_form_data)
    assertRedirects(
        response,
        reverse('blog:profile', args=(profile_form_data['username'],)),
    )

    new_user = User.objects.get(username=profile_form_data['username'])
    assert new_user.first_name == profile_form_data['first_name']
    assert new_user.last_name == profile_form_data['last_name']
    assert new_user.email == profile_form_data['email']


def test_anonymous_cant_create_post(
    client,
    post_form_data,
    post_create_url,
):
    Post.objects.all().delete()

    client.post(post_create_url, data=post_form_data)

    assert Post.objects.count() == 0


def test_user_can_create_post(
    user_client,
    post_form_data,
    post_create_url,
    user_profile_url,
):
    Post.objects.all().delete()

    response = user_client.post(post_create_url, data=post_form_data)
    assertRedirects(response, user_profile_url)

    assert Post.objects.count() == 1

    new_post = Post.objects.get()
    assert new_post.title == post_form_data['title']
    assert new_post.text == post_form_data['text']
    assert new_post.location.id == post_form_data['location']
    assert new_post.category.id == post_form_data['category']
    assert new_post.pub_date == post_form_data['pub_date']
    assert new_post.author == user_client.user
    assert new_post.image == post_form_data['image']


def test_anonymous_cant_add_comment(
    client,
    comment_form_data,
    comment_add_url,
):
    Comment.objects.all().delete()

    client.post(comment_add_url, data=comment_form_data)

    assert Comment.objects.count() == 0


def test_user_can_add_comment(
    user_client,
    post,
    comment_form_data,
    comment_add_url,
    post_detail_url,
):
    Comment.objects.all().delete()

    response = user_client.post(comment_add_url, data=comment_form_data)
    assertRedirects(response, post_detail_url)

    assert Comment.objects.count() == 1

    new_comment = Comment.objects.get()
    assert new_comment.text == comment_form_data['text']
    assert new_comment.post == post
    assert new_comment.author == user_client.user


def test_user_cant_edit_someones_post(
    user_client,
    post,
    post_edit_url,
    post_form_data,
):
    user_client.post(post_edit_url, data=post_form_data)

    new_post = Post.objects.get(pk=post.id)
    assert new_post.title == post.title
    assert new_post.text == post.text
    assert new_post.location == post.location
    assert new_post.category == post.category
    assert new_post.author == post.author
    assert new_post.image == post.image


def test_user_cant_edit_someones_comment(
    user_client,
    comment,
    comment_edit_url,
    comment_form_data,
):
    user_client.post(comment_edit_url, data=comment_form_data)

    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.text == comment.text
    assert new_comment.post == comment.post
    assert new_comment.author == comment.author


def test_author_can_edit_post(
    author_client,
    post,
    post_edit_url,
    post_form_data,
    post_detail_url,
):
    response = author_client.post(post_edit_url, data=post_form_data)
    assertRedirects(response, post_detail_url)

    new_post = Post.objects.get(pk=post.id)
    assert new_post.title == post_form_data['title']
    assert new_post.text == post_form_data['text']
    assert new_post.location.id == post_form_data['location']
    assert new_post.category.id == post_form_data['category']
    assert new_post.pub_date == post_form_data['pub_date']
    assert new_post.author == post.author
    assert new_post.image == post_form_data['image']


def test_author_can_edit_comment(
    author_client,
    comment,
    comment_edit_url,
    comment_form_data,
    post_detail_url,
):
    response = author_client.post(comment_edit_url, data=comment_form_data)
    assertRedirects(response, post_detail_url)

    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.text == comment_form_data['text']
    assert new_comment.post == comment.post
    assert new_comment.author == comment.author


@pytest.mark.parametrize(
    'param_client, can_delete',
    ((lf('user_client'), False), (lf('author_client'), True)),
)
@pytest.mark.parametrize(
    'url, model',
    (
        (lf('post_delete_url'), Post),
        (lf('comment_delete_url'), Comment),
    ),
)
def test_user_can_delete(param_client, url, model, can_delete):
    old_count = model.objects.count()

    param_client.delete(url)

    if can_delete:
        assert model.objects.count() == old_count - 1
    else:
        assert model.objects.count() == old_count
