from unittest.mock import MagicMock, patch

from discounterland.app.auth import replace_password_with_hash
from discounterland.auth.passwords import password_hash
from discounterland.auth.tokens import check_token


def test_hash_password():
    password = "unsecurepassword"
    account = {"username": "91nunocosta@gmail.com", "password": password}

    fake_hash = "fake_hash"

    password_hash_mock = MagicMock(return_value=fake_hash)

    with patch("discounterland.app.auth.password_hash", password_hash_mock):
        replace_password_with_hash([account])

    password_hash_mock.assert_called_with(password)

    assert account["password"] == fake_hash


def test_non_existing_account_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    response = client.post("login/", json=data)

    assert response.status_code == 401


def test_invalid_password_login(db, client, jwt_secret):
    db.accounts.drop()

    username = "91nunocosta@gmail.com"
    password = "notsecurepassword"

    data = {"username": username, "password": "invalid_password"}
    account = {"username": username, "password": password_hash(password)}

    db.accounts.insert_one(account)

    response = client.post("login/", json=data)

    assert response.status_code == 401


def test_valid_login(db, client, jwt_secret):
    db.accounts.drop()

    username = "91nunocosta@gmail.com"
    password = "notsecurepassword"

    data = {"username": username, "password": password}
    account = {"username": username, "password": password_hash(password)}

    db.accounts.insert_one(account)

    response = client.post("login/", json=data)

    assert response.status_code == 200

    data = response.json
    assert check_token(data["token"])["sub"] == username
