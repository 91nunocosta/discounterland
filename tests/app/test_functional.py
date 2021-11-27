from unittest.mock import patch

import pytest


@pytest.mark.skip(reason="promotion creation not implemented yet")
@patch.dict("os.environ", {"JWT_SECRET": "fake_secret"})
def test_authentication_functionality(clear_db, client):
    """
    Follows the following sequence:
    1. register a user
    2. login with that user
    3. create a task
    4. get list of task
    """
    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    response = client.post("/login", json=account)

    assert response.status_code == 200

    token = response.json["token"]

    response = client.post(
        "/brands/61a22c8f43cf71b9933afdd7/promotions",
        json={
            "expiration_date": "2022-11-25T16:51:02.003Z",
            "product": {
                "name": "Nutella",
            },
            "discounts_quantity": 10,
        },
        headers={"Authorization": token},
    )

    assert response.status_code == 201

    response = client.get("/tasks", headers={"Authorization": token})

    total_items = response.json["_meta"]["total"]

    assert total_items == 1
