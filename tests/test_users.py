def test_get_all_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_root_not_found(client):
    response = client.get("/randomroute")

    assert response.status_code == 404
