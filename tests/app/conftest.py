import datetime
from unittest.mock import patch

import pytest
import requests
import simplejson.errors

from discounterland.app import SETTINGS, create_app


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
def token(user):
    # the fixture is evaluated before each test who depend on it
    # then it is injected in the test (dependency injection)
    # in this case, after the test ends the context returns here
    # and continues after the yield expression

    # a patch for mocking the check_token function is started before the test
    # it is finished when the test stops
    token_payload = {"sub": user["username"]}

    patcher2 = patch(
        "discounterland.app.consumers.check_token", lambda _: token_payload
    )
    patcher3 = patch("discounterland.app.brands.check_token", lambda _: token_payload)

    patcher2.start()
    patcher3.start()

    yield "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI"  # noqa

    patcher2.stop()
    patcher3.stop()


@pytest.fixture
def clear_db(db):
    db.command("dropDatabase")
