from dateutil.parser import parse

from tests.app.helpers import items_without_meta


def test_add_promotion(db, client, token):
    db.promotions.drop()

    brand_id = "61a22c8f43cf71b9933afdd7"

    datestring = "2022-11-25T16:51:02.003Z"
    date = parse(datestring).replace(tzinfo=None)

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

    print(response.json)

    assert response.status_code == 201

    added_promotion = dict(db.promotions.find_one())

    added_promotion["expiration_date"] = added_promotion["expiration_date"].replace(
        tzinfo=None
    )

    print(added_promotion)

    assert items_without_meta([added_promotion]) == items_without_meta(
        [expected_response]
    )
