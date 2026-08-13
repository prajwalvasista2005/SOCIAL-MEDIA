from app import models, utils
def test_create_comment(
    authorized_client,
    test_post
):
    response = authorized_client.post(
        f"/comments/{test_post.id}",
        json={
            "content": "Nice post!"
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["content"] == "Nice post!"
def test_get_comments(
    client,
    test_comment,
    test_post
):
    response = client.get(
        f"/comments/{test_post.id}"
    )

    assert response.status_code == 200

def test_get_comments(
    client,
    test_comment,
    test_post
):
    response = client.get(
        f"/comments/{test_post.id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["content"] == "Test Comment"

def test_delete_comment_not_found(
    authorized_client
):
    response = authorized_client.delete(
        "/comments/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"