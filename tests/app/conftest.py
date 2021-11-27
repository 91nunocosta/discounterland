from unittest.mock import patch
import datetime

import pytest

from discounterland.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
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
          "creation_date": "2021-11-25T16:51:02.003Z",
          "expiration_date": datetime.datetime.now() + datetime.timedelta(years=2),
          "product": {
            "name": "Nutella",
            "images": [
              "https://images.jumpseller.com/store/hercules-it-llc/10188702/Nutella.jpg"
            ]
          },
          "discounts_quantity": 10
        }
    ).inserted_id

    return db.promotions.find_one({"_id": _id})


@pytest.fixture
def expired_promotion(db):
    _id = db.promotions.insert_one(
        {
          "id": "/promotions/20211fcf-0116-4217-9816-be11a4954344",
          "brand_id": "/brands/745ba01d-51a1-4615-9571-ee14d15bb4af",
          "creation_date": "2020-11-25T16:51:02.003Z",
          "expiration_date": "2020-11-25T16:51:02.003Z",
          "product": {
            "name": "Nutella",
            "images": [
              "https://images.jumpseller.com/store/hercules-it-llc/10188702/Nutella.jpg"
            ]
          },
          "discounts_quantity": 10
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

    patcher1 = patch("discounterland.app.auth.check_token", lambda _: token_payload)
    patcher2 = patch("discounterland.app.consumers.check_token", lambda _: token_payload)
    patcher3 = patch("discounterland.app.brands.check_token", lambda _: token_payload)

    patcher1.start()
    patcher2.start()
    patcher3.start()

    yield token_payload

    patcher1.stop()
    patcher2.stop()
    patcher3.stop()


@pytest.fixture
def clear_db(db):
    db.command("dropDatabase")
