from app import models
from datetime import datetime, timedelta
def test_login_returns_refresh_token(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_refresh_token_returns_new_access_token(
    client,
    test_user
):
    login_response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_refresh_token_invalid_token(client):
    response = client.post(
        "/refresh",
        json={
            "refresh_token": "invalid_token"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"

def test_logout_revokes_refresh_token(
    client,
    test_user
):
    login_response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    logout_response = client.post(
        "/logout",
        json={
            "refresh_token": refresh_token
        }
    )

    assert logout_response.status_code == 200

    refresh_response = client.post(
        "/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Invalid refresh token"

def test_logout_invalid_token(client):
    response = client.post(
        "/logout",
        json={
            "refresh_token": "invalid_token"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"

def test_user_can_have_multiple_refresh_tokens(
    client,
    test_user
):
    login_1 = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    login_2 = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    refresh_token_1 = login_1.json()["refresh_token"]
    refresh_token_2 = login_2.json()["refresh_token"]

    assert refresh_token_1 != refresh_token_2

def test_logout_revokes_only_one_refresh_token(
    client,
    test_user
):
    login_1 = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    login_2 = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    refresh_token_1 = login_1.json()["refresh_token"]
    refresh_token_2 = login_2.json()["refresh_token"]

    logout_response = client.post(
        "/logout",
        json={
            "refresh_token": refresh_token_1
        }
    )

    assert logout_response.status_code == 200

    revoked_token_response = client.post(
        "/refresh",
        json={
            "refresh_token": refresh_token_1
        }
    )

    valid_token_response = client.post(
        "/refresh",
        json={
            "refresh_token": refresh_token_2
        }
    )

    assert revoked_token_response.status_code == 401
    assert valid_token_response.status_code == 200