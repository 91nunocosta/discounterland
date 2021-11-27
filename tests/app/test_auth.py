from unittest.mock import MagicMock, patch

from discounterland.app.auth import replace_password_with_hash


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


def test_invalid_password_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    db.accounts.insert_one(dict(data))

    with patch("discounterland.app.auth.check_password", lambda _a, _b: False):
        response = client.post("login/", json=data)

    assert response.status_code == 401


def test_valid_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    db.accounts.insert_one(dict(data))

    fake_token = "this_is_a_fake_token"

    with patch("discounterland.app.auth.generate_token", lambda _: fake_token):
        with patch("discounterland.app.auth.check_password", lambda _a, _b: True):
            response = client.post("login/", json=data)

    assert response.status_code == 200

    data = response.json
    assert data["token"] == fake_token
