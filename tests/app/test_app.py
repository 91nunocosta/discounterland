def test_get_root(client, token):
    response = client.get("/", headers={"Authorization": token})

    assert response.status_code == 200
