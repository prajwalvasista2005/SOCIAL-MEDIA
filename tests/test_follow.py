from app import models, utils
def test_follow_user(
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

    response = authorized_client.post(
        "/follow",
        json={
            "following_id": other_user.id
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Successfully followed user"

def test_follow_nonexistent_user(
    authorized_client
):
    response = authorized_client.post(
        "/follow",
        json={
            "following_id": 99999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_follow_yourself(
    authorized_client,
    test_user
):
    response = authorized_client.post(
        "/follow",
        json={
            "following_id": test_user.id
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot follow yourself"

def test_follow_same_user_twice(
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

    authorized_client.post(
        "/follow",
        json={
            "following_id": other_user.id
        }
    )

    response = authorized_client.post(
        "/follow",
        json={
            "following_id": other_user.id
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Already following this user"

def test_unfollow_user(
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

    authorized_client.post(
        "/follow",
        json={
            "following_id": other_user.id
        }
    )

    response = authorized_client.delete(
        f"/follow/{other_user.id}"
    )

    assert response.status_code == 204

def test_unfollow_user_not_following(
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

    response = authorized_client.delete(
        f"/follow/{other_user.id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "You are not following this user"