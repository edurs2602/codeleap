import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_post(db):
    def make_post(username="john_doe", title="My first post", content="Hello!"):
        return Post.objects.create(username=username, title=title, content=content)

    return make_post


@pytest.mark.django_db
def test_create_post(api_client):
    url = reverse("post-list")  # ViewSet list/create
    data = {
        "username": "john_doe",
        "title": "My first post",
        "content": "Hello, this is my first post!",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "john_doe"


@pytest.mark.django_db
def test_list_posts(api_client, create_post):
    post = create_post()
    url = reverse("post-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == post.id


@pytest.mark.django_db
def test_list_posts_filtered_by_username(api_client, create_post):
    create_post(username="john_doe")
    create_post(username="jane_doe")
    url = reverse("post-list") + "?username=jane_doe"
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["username"] == "jane_doe"


@pytest.mark.django_db
def test_partial_update_post(api_client, create_post):
    post = create_post()
    url = reverse("post-detail", kwargs={"pk": post.id})
    data = {"title": "Updated title"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["title"] == "Updated title"


@pytest.mark.django_db
def test_delete_post(api_client, create_post):
    post = create_post()
    url = reverse("post-detail", kwargs={"pk": post.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Post.objects.filter(id=post.id).count() == 0


@pytest.mark.django_db
def test_like_unlike_post(api_client, create_post):
    post = create_post()
    like_url = reverse("post-like", kwargs={"pk": post.id})
    unlike_url = reverse("post-unlike", kwargs={"pk": post.id})

    # Like
    response = api_client.post(like_url)
    assert response.status_code == 200
    assert response.data["status"] == "liked"

    # Unlike
    response = api_client.post(unlike_url)
    assert response.status_code == 200
    assert response.data["status"] == "unliked"


@pytest.mark.django_db
def test_create_comment(api_client, create_post):
    post = create_post()
    url = reverse("post-comments-create", kwargs={"post_id": post.id})
    data = {"username": "me123", "content": "This is a comment"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["content"] == "This is a comment"
    assert response.data["post"] == post.id
