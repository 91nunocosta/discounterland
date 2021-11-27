import json
import random
import string
import datetime
from bson import ObjectId
from flask import current_app, abort

from discounterland.app.settings import SETTINGS


def _serialize_date(date):
    return date.strftime(SETTINGS["DATE_FORMAT"])


def _get_db():
    return current_app.data.driver.db


def _get_promotion(promotion_id):
    promotions = _get_db().promotions

    return promotions.find_one({"_id": ObjectId(promotion_id)})


def check_promotion(items):
    
    for item in items:
        promotion_id = item["promotion_id"]

        promotion = _get_promotion(promotion_id)

        if promotion is None:
            abort(422)

        expiration_date = promotion["expiration_date"]

        now = datetime.datetime.now().replace(tzinfo=expiration_date.tzinfo)

        if expiration_date < now:
            return abort(422)


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
    promotion["expiration_date"] = _serialize_date(promotion["expiration_date"])

    print(promotion)

    body["expiration_date"] = promotion["expiration_date"]
    body["promotion"] = promotion

    payload.data = json.dumps(body)
