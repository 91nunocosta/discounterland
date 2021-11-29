import datetime

from bson import ObjectId
from dateutil.parser import parse

from discounterland.app.discounts import _serialize_date
from tests.app.helpers import items_without_meta


def test_add_promotion(db, client, token, user):
    db.promotions.drop()

    user_id = user["_id"]

    brand_id = "61a22c8f43cf71b9933afdd7"

    db.brands.insert_one({"_id": brand_id})

    # user needs to be one of the brand's manager
    db.brand_managers.insert_one(
        {
            "brand_id": ObjectId(brand_id),
            "account_id": user_id,
        }
    )

    datestring = _serialize_date(datetime.datetime.now() + datetime.timedelta(days=1))
    date = parse(datestring).replace(tzinfo=None).replace(microsecond=0)

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 10,
    }

    expected_response = dict(promotion)

    # the test client library gets the dates as datetime objects
    expected_response["expiration_date"] = date

    # the promotion is created with the brand id from the path
    expected_response["brand_id"] = brand_id

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": token},
    )

    assert response.status_code == 201

    added_promotion = dict(db.promotions.find_one())

    added_promotion["expiration_date"] = (
        added_promotion["expiration_date"].replace(tzinfo=None).replace(microsecond=0)
    )

    assert items_without_meta([added_promotion]) == items_without_meta(
        [expected_response]
    )


def test_add_promotion_for_non_authenticated_user(db, client):
    db.promotions.drop()

    brand_id = "61a22c8f43cf71b9933afdd7"

    datestring = "2022-11-25T16:51:02.003Z"

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 10,
    }

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
    )

    assert response.status_code == 401


def test_add_promotion_with_non_authorized_user(db, client, token):
    db.promotions.drop()

    brand_id = "61a22c8f43cf71b9933afdd7"

    datestring = "2022-11-25T16:51:02.003Z"

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 10,
    }

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": token},
    )

    assert response.status_code == 401


def test_add_promotion_with_past_expiration_date(db, client, token, user):
    db.promotions.drop()

    user_id = user["_id"]

    brand_id = "61a22c8f43cf71b9933afdd7"

    db.brands.insert_one({"_id": brand_id})

    # user needs to be one of the brand's manager
    db.brand_managers.insert_one(
        {
            "brand_id": ObjectId(brand_id),
            "account_id": user_id,
        }
    )

    datestring = "2020-11-25T16:51:02.003Z"

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 10,
    }

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": token},
    )

    assert response.status_code == 422


def test_add_promotion_with_non_positive_discount_quantity(db, client, token, user):
    db.promotions.drop()

    user_id = user["_id"]

    brand_id = "61a22c8f43cf71b9933afdd7"

    db.brands.insert_one({"_id": brand_id})

    # user needs to be one of the brand's manager
    db.brand_managers.insert_one(
        {
            "brand_id": ObjectId(brand_id),
            "account_id": user_id,
        }
    )

    datestring = _serialize_date(datetime.datetime.now() + datetime.timedelta(days=1))

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 0,
    }

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": token},
    )

    assert response.status_code == 422


def test_add_promotion_with_non_url_product_image(db, client, token, user):
    db.promotions.drop()

    user_id = user["_id"]

    brand_id = "61a22c8f43cf71b9933afdd7"

    db.brands.insert_one({"_id": brand_id})

    # user needs to be one of the brand's manager
    db.brand_managers.insert_one(
        {
            "brand_id": ObjectId(brand_id),
            "account_id": user_id,
        }
    )

    datestring = _serialize_date(datetime.datetime.now() + datetime.timedelta(days=1))
    date = parse(datestring).replace(tzinfo=None).replace(microsecond=0)

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": ["images.jumpseller/store/hercules-it-llc/10188702/Nutella.jpg"],
        },
        "discounts_quantity": 10,
    }

    expected_response = dict(promotion)

    # the test client library gets the dates as datetime objects
    expected_response["expiration_date"] = date

    # the promotion is created with the brand id from the path
    expected_response["brand_id"] = brand_id

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": token},
    )

    assert response.status_code == 422


def test_add_promotion_with_invalid_auth_token(db, client, jwt_secret, user):
    db.promotions.drop()

    user_id = user["_id"]

    brand_id = "61a22c8f43cf71b9933afdd7"

    db.brands.insert_one({"_id": brand_id})

    # user needs to be one of the brand's manager
    db.brand_managers.insert_one(
        {
            "brand_id": ObjectId(brand_id),
            "account_id": user_id,
        }
    )

    datestring = _serialize_date(datetime.datetime.now() + datetime.timedelta(days=1))

    promotion = {
        "expiration_date": datestring,
        "product": {
            "name": "Nutella",
            "images": [
                "https://images.jumpseller.com/store/hercules-it-llc/10188702/"
                "Nutella.jpg"
            ],
        },
        "discounts_quantity": 10,
    }

    response = client.post(
        f"/brands/{brand_id}/promotions",
        json=promotion,
        headers={"Authorization": "invalid_token"},
    )

    assert response.status_code == 401
