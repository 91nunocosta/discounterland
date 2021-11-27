from tests.app.helpers import items_without_meta


def test_add_discount(db, client, token):
    db.discounts.drop()

    promotion_id = "61a22c8f43cf71b9933afdd7"
    consumer_id = "61a22cb797321cee10c8df49"

    discount = {
        "promotion_id": promotion_id,
    }

    expected_response = dict(discount)

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
        headers={"authorization": token},
    )

    assert response.status_code == 201

    added_discount = dict(db.discounts.find_one())

    assert items_without_meta([added_discount]) == items_without_meta(
        [expected_response]
    )


def test_add_discount_for_non_authenticated_user(db, client):
    db.discounts.drop()

    promotion_id = "61a22c8f43cf71b9933afdd7"
    consumer_id = "61a22cb797321cee10c8df49"

    discount = {
        "promotion_id": promotion_id,
    }

    response = client.post(
        f"/consumers/{consumer_id}/discounts",
        json=discount,
    )

    assert response.status_code == 401

