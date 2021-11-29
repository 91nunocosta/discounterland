from discounterland.auth.passwords import check_password


def test_add_account(db, client):
    db.accounts.drop()

    username = "91nunocosta@gmail.com"
    password = "unsecurepassword"
    account = {"username": username, "password": password}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    added_account = db.accounts.find_one()

    assert added_account.get("username") == username
    assert check_password(password, added_account.get("password"))


def test_add_duplicate(db, client):
    db.accounts.drop()

    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    response = client.post("/accounts", json=account)

    assert response.status_code == 422

    assert db.accounts.count() == 1
