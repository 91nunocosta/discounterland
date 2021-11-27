import json
import random
import string
from bson import ObjectId
from flask import current_app, abort


def _get_db():
    return current_app.data.driver.db


def _get_promotion(promotion_id):
    promotions = _get_db().promotions

    return promotions.find_one({"_id": ObjectId(promotion_id)})


def check_promotion(items):
    
    for item in items:
        promotion_id = item["promotion_id"]

        result = _get_promotion(promotion_id)

        if result is None:
            abort(422)


def _char() -> str:
    return random.choice(string.ascii_uppercase + string.digits)


def _word() -> str:
    return "".join(_char() for _ in range(4))


def _generate_code() -> str:
    return "-".join(_word() for _ in range(4))


def add_code(items):
    for item in items:

        item["code"] = _generate_code()


def add_promotion_details(request, payload):
    body = json.loads(payload.data)

    discount_id = body["_id"]

    discount = _get_db().discounts.find_one({"_id": ObjectId(discount_id)})

    body["code"] = discount["code"]

    promotion_id = request.json["promotion_id"]

    promotion = _get_promotion(promotion_id)

    promotion["_id"] = str(promotion["_id"])

    body["expiration_date"] = promotion["expiration_date"]
    body["promotion"] = promotion

    payload.data = json.dumps(body)
