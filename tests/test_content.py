import pytest
from pytest_lazyfixture import lazy_fixture as lf

from blog.constants import POSTS_ON_PAGE
from blog.forms import CommentForm, PostForm, ProfileForm


@pytest.mark.usefixtures('create_many_posts')
@pytest.mark.parametrize(
    'url',
    (
        lf('index_url'),
        lf('category_url'),
        lf('a_profile_url'),
    ),
)
def test_page_contains_exact_post_count(client, url):
    assert client.get(url).context['object_list'].count() == POSTS_ON_PAGE


@pytest.mark.usefixtures('create_many_posts')
@pytest.mark.parametrize(
    'url',
    (
        lf('index_url'),
        lf('category_url'),
        lf('a_profile_url'),
    ),
)
def test_post_ordering(client, url):
    response = client.get(url)
    post_dates = [post.pub_date for post in response.context['object_list']]
    ordered_posts = sorted(post_dates, reverse=True)
    assert post_dates == ordered_posts


@pytest.mark.usefixtures('create_many_comments')
def test_comment_ordering(client, post_detail_url):
    response = client.get(post_detail_url)
    comment_times = [
        comment.created_at
        for comment in response.context['post'].comments.all()
    ]
    ordered_times = sorted(comment_times)

    assert comment_times == ordered_times


def test_detail_has_no_comment_form_for_anon(client, post_detail_url):
    response = client.get(post_detail_url)
    assert 'form' not in response.context


@pytest.mark.parametrize(
    'url, form_class',
    (
        (lf('profile_edit_url'), ProfileForm),
        (lf('post_create_url'), PostForm),
        (lf('post_edit_url'), PostForm),
        (lf('post_detail_url'), CommentForm),
        (lf('comment_edit_url'), CommentForm),
    ),
)
def test_page_contains_form(author_client, url, form_class):
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], form_class)


post_contain_params = (
    (lf('post'), lf('index_url'), lf('user_client'), True),
    (lf('post'), lf('category_url'), lf('user_client'), True),
    (lf('post'), lf('other_category_url'), lf('user_client'), False),
    (lf('post'), lf('a_profile_url'), lf('user_client'), True),
    (lf('post'), lf('user_profile_url'), lf('user_client'), False),
    (lf('unpublished_post'), lf('index_url'), lf('user_client'), False),
    (lf('unpublished_post'), lf('index_url'), lf('author_client'), False),
    (lf('delayed_post'), lf('index_url'), lf('user_client'), False),
    (lf('delayed_post'), lf('index_url'), lf('author_client'), False),
    (lf('unpub_cat_post'), lf('index_url'), lf('user_client'), False),
    (lf('unpub_cat_post'), lf('index_url'), lf('author_client'), False),
    (lf('unpublished_post'), lf('category_url'), lf('user_client'), False),
    (lf('unpublished_post'), lf('category_url'), lf('author_client'), False),
    (lf('delayed_post'), lf('category_url'), lf('user_client'), False),
    (lf('delayed_post'), lf('category_url'), lf('author_client'), False),
    (lf('unpublished_post'), lf('a_profile_url'), lf('user_client'), False),
    (lf('unpublished_post'), lf('a_profile_url'), lf('author_client'), True),
    (lf('delayed_post'), lf('a_profile_url'), lf('user_client'), False),
    (lf('delayed_post'), lf('a_profile_url'), lf('author_client'), True),
    (lf('unpub_cat_post'), lf('a_profile_url'), lf('user_client'), False),
    (lf('unpub_cat_post'), lf('a_profile_url'), lf('author_client'), True),
)


@pytest.mark.parametrize(
    'param_post, url, param_client, does_show',
    post_contain_params,
)
def test_contains_post(param_post, url, param_client, does_show):
    response = param_client.get(url)
    assert (param_post in response.context['object_list']) is does_show
