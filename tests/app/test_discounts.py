import re
from tests.app.helpers import items_without_meta
from discounterland.app.discounts import _serialize_date


WORD = "[0-9A-Z]{4,4}"


def _is_valid_code(code: str) -> bool:
    return re.fullmatch(f"{WORD}-{WORD}-{WORD}-{WORD}", code) is not None


def test_add_discount(db, client, token, user, promotion):
    promotion_id = str(promotion["_id"])
    consumer_id = user["_id"]

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 201

    response_body = items_without_meta([response.json])[0]

    assert set(response_body) == {"promotion", "code", "expiration_date"}

    promotion["_id"] = str(promotion["_id"])
    promotion["expiration_date"] = _serialize_date(promotion["expiration_date"])

    assert response_body["promotion"] == promotion

    assert response_body["expiration_date"] == promotion["expiration_date"]

    assert _is_valid_code(response_body["code"])

    added_discount = dict(db.discounts.find_one())

    assert (set(items_without_meta([added_discount])[0].keys())
            == {"promotion_id", "code"})

    assert added_discount["promotion_id"] == promotion_id 

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

    consumer_id = db.accounts.insert_one({
        "username": "someone",
        "password": "insecurepass",
    }).inserted_id

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


