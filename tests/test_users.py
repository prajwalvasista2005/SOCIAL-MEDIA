from app import models, utils
def test_get_all_users(client, test_user):
    response = client.get("/users")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["email"] == test_user.email
    assert data[0]["username"] == test_user.username
def test_root_not_found(client):
    response = client.get("/randomroute")

    assert response.status_code == 404
def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "email": "newuser@gmail.com",
            "password": "password123",
            "username": "newuser"
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "newuser@gmail.com"
    assert data["username"] == "newuser"

def test_create_user_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "email": "not-an-email",
            "password": "password123",
            "username": "newuser"
        }
    )

    assert response.status_code == 422

def test_create_duplicate_user(client):
    payload = {
        "email": "duplicate@gmail.com",
        "password": "password123",
        "username": "duplicateuser"
    }

    client.post("/users", json=payload)

    response = client.post("/users", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

 
def test_get_user(test_user, client):
    response = client.get(f"/users/{test_user.id}")

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username
    assert data["followers_count"] == 0
    assert data["following_count"] == 0

def test_get_user_not_found(client):
    response = client.get("/users/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 99999 does not exist"

def test_login_token(token):
    assert token is not None

def test_authorized_client(authorized_client):
    assert authorized_client.headers.get("Authorization") is not None

def test_update_user(
    authorized_client,
    test_user
):
    response = authorized_client.put(
        f"/users/{test_user.id}",
        json={
            "email": "updated@gmail.com",
            "password": "newpassword123"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "updated@gmail.com"

def test_update_other_user_forbidden(
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

    response = authorized_client.put(
        f"/users/{other_user.id}",
        json={
            "email": "hacked@gmail.com",
            "password": "newpassword"
        }
    )

    assert response.status_code == 403

def test_delete_user(
    authorized_client,
    test_user
):
    response = authorized_client.delete(
        f"/users/{test_user.id}"
    )

    assert response.status_code == 204

def test_delete_other_user_forbidden(
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
        f"/users/{other_user.id}"
    )

    assert response.status_code == 403

def test_delete_user_not_found(
    authorized_client
):
    response = authorized_client.delete(
        "/users/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "The user with id 99999 was not found"

def test_update_user_not_found(
    authorized_client
):
    response = authorized_client.put(
        "/users/99999",
        json={
            "email": "updated@gmail.com",
            "password": "newpassword123"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 99999 does not exist"

def test_update_other_user(
    authorized_client,
    session
):
    other_user = models.User(
        email="other@gmail.com",
        username="otheruser",
        password="hashedpassword"
    )

    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    response = authorized_client.put(
        f"/users/{other_user.id}",
        json={
            "email": "hacked@gmail.com",
            "password": "newpassword123"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"