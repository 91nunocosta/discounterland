import re

from bson import ObjectId

import discounterland.auth.tokens
from discounterland.app.discounts import _serialize_date
from tests.app.helpers import items_without_meta

WORD = "[0-9A-Z]{4,4}"


def _is_valid_code(code: str) -> bool:
    return re.fullmatch(f"{WORD}-{WORD}-{WORD}-{WORD}", code) is not None


def jsonify(data):
    if isinstance(data, ObjectId):
        return str(data)

    if isinstance(data, dict):
        return {key: jsonify(value) for key, value in data.items()}

    if isinstance(data, list):
        return [jsonify(item) for item in data]

    return data


def test_add_discount(db, client, token, user, promotion):
    promotion_id = promotion["_id"]
    consumer_id = user["_id"]

    payload = jsonify(
        {
            "promotion_id": promotion_id,
        }
    )

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=payload,
        headers={"authorization": token},
    )

    assert response.status_code == 201

    response_body = items_without_meta([response.json])[0]

    assert set(response_body) == {"promotion", "code", "expiration_date"}

    promotion["_id"] = promotion["_id"]
    promotion["expiration_date"] = _serialize_date(promotion["expiration_date"])

    assert response_body["promotion"] == jsonify(promotion)

    assert response_body["expiration_date"] == promotion["expiration_date"]

    assert _is_valid_code(response_body["code"])

    added_discount = dict(db.discounts.find_one())

    assert set(items_without_meta([added_discount])[0].keys()) == {
        "promotion_id",
        "code",
        "consumer_id",
    }

    assert added_discount["promotion_id"] == promotion_id

    assert added_discount.get("consumer_id") == consumer_id

    assert re.fullmatch(f"{WORD}-{WORD}-{WORD}-{WORD}", added_discount["code"])


def test_add_discount_for_non_authenticated_user(db, client, promotion):
    db.discounts.drop()

    promotion_id = str(promotion["_id"])
    consumer_id = "61a22cb797321cee10c8df49"

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
    )

    assert response.status_code == 401


def test_add_discount_for_unauthorized_user(db, client, token, promotion):
    db.discounts.drop()

    consumer_id = db.accounts.insert_one(
        {
            "username": "someone",
            "password": "insecurepass",
        }
    ).inserted_id

    promotion_id = str(promotion["_id"])

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 401


def test_add_discount_for_non_existing_consumer(db, client, token, promotion):
    db.discounts.drop()

    promotion_id = str(promotion["_id"])

    consumer_id = "61a28cbb7cc480477ff9ea88"

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 401


def test_add_discount_for_non_existing_promotion(db, client, token, user):
    db.discounts.drop()

    promotion_id = "61a29601629ceafe6030c511"
    consumer_id = user["_id"]

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 422


def test_add_discount_for_expired_promotion(db, client, token, user, expired_promotion):
    promotion_id = str(expired_promotion["_id"])
    consumer_id = user["_id"]

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 422


def test_add_discount_after_no_more_discounts_available(
    db, client, promotion, jwt_secret
):
    promotion_id = str(promotion["_id"])

    discount = {
        "promotion_id": promotion_id,
    }

    for i in range(promotion["discounts_quantity"] + 1):

        username = f"user{i}"

        consumer_id = str(
            db.accounts.insert_one(
                {
                    "username": username,
                    "password": "insecurepass",
                }
            ).inserted_id
        )

        token = discounterland.auth.tokens.generate_token(username)

        response = client.post(
            f"/consumers/{consumer_id}/discounts",
            json=discount,
            headers={"authorization": f"Bearer {token}"},
        )

    assert response.status_code == 422


def test_add_discount_twice_for_same_consumer(db, client, token, user, promotion):
    promotion_id = str(promotion["_id"])
    consumer_id = user["_id"]

    discount = {
        "promotion_id": promotion_id,
    }

    for _ in range(2):

        response = client.post(
            f"/consumers/{consumer_id}/discounts",
            json=discount,
            headers={"authorization": token},
        )

    assert response.status_code == 422


def test_add_discount_for_invalid_promotion_id(db, client, token, user):
    consumer_id = user["_id"]

    discount = {
        "promotion_id": "invalid_promotion_id",
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 422


def test_add_discount_for_invalid_auth_token(db, client, user, jwt_secret):
    consumer_id = user["_id"]

    discount = {
        "promotion_id": "invalid_promotion_id",
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": "invalid_token"},
    )

    assert response.status_code == 401
