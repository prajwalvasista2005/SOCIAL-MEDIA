from app import models, utils


def test_create_post(
    authorized_client
):
    response = authorized_client.post(
        "/sqlalchemy",
        json={
            "title": "My First Post",
            "content": "Hello World",
            "published": True
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "My First Post"
    assert data["content"] == "Hello World"

def test_create_post_unauthorized(client):
    response = client.post(
        "/sqlalchemy",
        json={
            "title": "My First Post",
            "content": "Hello World",
            "published": True
        }
    )

    assert response.status_code == 401

def test_get_post(
    authorized_client,
    test_post
):
    response = authorized_client.get(
        f"/sqlalchemy/{test_post.id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["post"]["id"] == test_post.id
    assert data["post"]["title"] == test_post.title
    assert data["post"]["content"] == test_post.content

def test_get_post_not_found(
    authorized_client
):
    response = authorized_client.get(
        "/sqlalchemy/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"

def test_get_all_posts(
    authorized_client,
    test_posts
):
    response = authorized_client.get("/sqlalchemy")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2

def test_get_all_posts_limit(
    authorized_client,
    test_posts
):
    response = authorized_client.get(
        "/sqlalchemy?limit=1"
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1

def test_get_all_posts_skip(
    authorized_client,
    test_posts
):
    response = authorized_client.get(
        "/sqlalchemy?skip=1"
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1

def test_update_post(
    authorized_client,
    test_post
):
    response = authorized_client.put(
        f"/sqlalchemy/{test_post.id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": True
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"

def test_update_post_not_found(
    authorized_client
):
    response = authorized_client.put(
        "/sqlalchemy/99999",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"

def test_update_other_users_post(
    authorized_client,
    session
):
    other_user = models.User(
        email="other@gmail.com",
        username="otheruser",
        password=utils.hash("password123")
    )

    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    other_post = models.Post(
        title="Other Post",
        content="Other Content",
        owner_id=other_user.id
    )

    session.add(other_post)
    session.commit()
    session.refresh(other_post)

    response = authorized_client.put(
        f"/sqlalchemy/{other_post.id}",
        json={
            "title": "Hacked",
            "content": "Hacked Content",
            "published": True
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"

def test_delete_post(
    authorized_client,
    test_post
):
    response = authorized_client.delete(
        f"/sqlalchemy/{test_post.id}"
    )

    assert response.status_code == 204

def test_delete_post_not_found(
    authorized_client
):
    response = authorized_client.delete(
        "/sqlalchemy/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"

def test_delete_other_users_post(
    authorized_client,
    session
):
    other_user = models.User(
        email="other@gmail.com",
        username="otheruser",
        password=utils.hash("password123")
    )

    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    other_post = models.Post(
        title="Other Post",
        content="Other Content",
        owner_id=other_user.id
    )

    session.add(other_post)
    session.commit()
    session.refresh(other_post)

    response = authorized_client.delete(
        f"/sqlalchemy/{other_post.id}"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"

def test_vote_on_post(
    authorized_client,
    test_post
):
    response = authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 1
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Successfully added vote"

def test_vote_twice(
    authorized_client,
    test_post
):
    authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 1
        }
    )

    response = authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 1
        }
    )

    assert response.status_code == 409

def test_vote_nonexistent_post(
    authorized_client
):
    response = authorized_client.post(
        "/vote",
        json={
            "post_id": 99999,
            "dir": 1
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Post with id 99999 does not exist"
    )
def test_delete_vote(
    authorized_client,
    test_post
):
    authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 1
        }
    )

    response = authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 0
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == (
        "Successfully deleted vote"
    )
def test_delete_vote_not_exist(
    authorized_client,
    test_post
):
    response = authorized_client.post(
        "/vote",
        json={
            "post_id": test_post.id,
            "dir": 0
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vote does not exist"