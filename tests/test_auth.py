def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200
def test_login_wrong_email(client):
    response = client.post(
        "/login",
        data={
            "username": "doesnotexist@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"

def test_login_wrong_password(
    client,
    test_user
):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid Credentials"

def test_login_returns_token(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"