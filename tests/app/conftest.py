import datetime
import os

import pytest
import requests
import simplejson.errors

from discounterland.app import SETTINGS, create_app
from discounterland.auth.tokens import generate_token


@pytest.fixture
def app():
    return create_app()


class RequestsClient:
    def __init__(self, host):
        self.host = host

    def _url(self, path):
        if not path.startswith("/"):
            path = "/" + path

        return self.host + path

    def _add_json_property(self, response):
        try:
            json = response.json()

            response.json = json
        except simplejson.errors.JSONDecodeError:
            pass

    def get(self, path, headers=None):
        if headers is None:
            headers = {}

        response = requests.get(self._url(path), headers=headers)

        self._add_json_property(response)

        return response

    def post(self, path, json=None, headers=None):
        if json is None:
            json = {}

        if headers is None:
            headers = {}

        response = requests.post(self._url(path), json=json, headers=headers)

        self._add_json_property(response)

        return response


@pytest.fixture
def client(functional, app):

    if functional:
        return RequestsClient("http://" + SETTINGS["SERVER_NAME"])

    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        db = app.data.driver.db
        db.command("dropDatabase")
        return db


@pytest.fixture
def user(db):
    _id = db.accounts.insert_one(
        {
            "username": "91nunocosta@gmail.com",
            "password": "insecurepassword",
        }
    ).inserted_id

    return db.accounts.find_one({"_id": _id})


@pytest.fixture
def promotion(db):
    _id = db.promotions.insert_one(
        {
            "id": "/promotions/20211fcf-0116-4217-9816-be11a4954344",
            "brand_id": "/brands/745ba01d-51a1-4615-9571-ee14d15bb4af",
            "expiration_date": datetime.datetime.now() + datetime.timedelta(days=365),
            "product": {
                "name": "Nutella",
                "images": [
                    "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                    "Nutella.jpg"
                ],
            },
            "discounts_quantity": 10,
        }
    ).inserted_id

    return db.promotions.find_one({"_id": _id})


@pytest.fixture
def expired_promotion(db):
    _id = db.promotions.insert_one(
        {
            "id": "/promotions/20211fcf-0116-4217-9816-be11a4954344",
            "brand_id": "/brands/745ba01d-51a1-4615-9571-ee14d15bb4af",
            "expiration_date": datetime.datetime(2020, 11, 25, 16),
            "product": {
                "name": "Nutella",
                "images": [
                    "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                    "Nutella.jpg"
                ],
            },
            "discounts_quantity": 10,
        }
    ).inserted_id

    return db.promotions.find_one({"_id": _id})


@pytest.fixture
def another_user():
    return "william.dev@example.com"


@pytest.fixture
def jwt_secret(user):
    if "JWT_SECRET" in os.environ:
        return

    secret = "Tz7NqafQAPs4pwbhvp2w9zx7XE3smTwZ2OMA6unVs_L43QjSVY2T-xvF65w9A88FXv2GsUwJZBcPUiX0qbkkY6MDYVjS02PWd0o3OzQN_P1vFrAmcPFfzvnI9fgxVvboPwRnFCNzOACbegAN8J4FBTb0cy1r3WYUu0ZurS3nsM76h5dCdOQL97TmDsdqugRgAk16pfEna1pZ1U4HfjnKv8KebbX1qx_jYlIPJHbNDGsidLmXbTb5y4ApZQMr9w1uUyFhdRitYIlNQ2U3rFkZ6Xc1w5UPlvcL_QEnINaLwJVm-lKnPDJ67yhnRyd2uGRN0MDrfZXt8YTN2hIJ9fMoVQ"  # noqa
    os.environ["JWT_SECRET"] = secret


@pytest.fixture
def token(user, jwt_secret):
    username = user["username"]

    token_value = generate_token(username)

    return f"Bearer {token_value}"


@pytest.fixture
def clear_db(db):
    db.command("dropDatabase")
