from unittest.mock import MagicMock, patch

from tests.app.helpers import items_without_meta


def test_add_account(db, client):
    db.accounts.drop()

    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    fake_hash = "fake_token"
    password_hash_mock = MagicMock(return_value=fake_hash)

    with patch("discounterland.app.auth.password_hash", password_hash_mock):
        response = client.post("/accounts", json=account)

    assert response.status_code == 201

    # password should be replaced by the corresponding hash
    account["password"] = fake_hash

    added_account = db.accounts.find_one()
    assert items_without_meta([added_account]) == items_without_meta([account])


def test_add_duplicate(db, client):
    db.accounts.drop()

    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    response = client.post("/accounts", json=account)

    assert response.status_code == 422

    assert db.accounts.count() == 1
