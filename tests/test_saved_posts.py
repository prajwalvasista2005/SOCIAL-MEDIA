from app import models, utils
def test_save_post(
    authorized_client,
    test_post
):
    response = authorized_client.post(
        f"/saved/{test_post.id}"
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Post saved successfully"
def test_save_nonexistent_post(
    authorized_client
):
    response = authorized_client.post(
        "/saved/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"

def test_save_post_twice(
    authorized_client,
    test_post
):
    authorized_client.post(
        f"/saved/{test_post.id}"
    )

    response = authorized_client.post(
        f"/saved/{test_post.id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Post already saved"

def test_get_saved_posts(
    authorized_client,
    test_post
):
    authorized_client.post(
        f"/saved/{test_post.id}"
    )

    response = authorized_client.get(
        "/saved"
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["post"]["id"] == test_post.id

def test_unsave_post(
    authorized_client,
    test_post
):
    authorized_client.post(
        f"/saved/{test_post.id}"
    )

    response = authorized_client.delete(
        f"/saved/{test_post.id}"
    )

    assert response.status_code == 204

def test_unsave_post_not_saved(
    authorized_client,
    test_post
):
    response = authorized_client.delete(
        f"/saved/{test_post.id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Post is not saved"

def test_get_saved_posts_empty(
    authorized_client
):
    response = authorized_client.get(
        "/saved"
    )

    assert response.status_code == 200
    assert response.json() == []