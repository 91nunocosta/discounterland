import datetime
import json
import random
import string

from bson import ObjectId
from flask import abort, current_app, make_response, request

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
            response = make_response("Promotion not found", 422)
            abort(response)

        expiration_date = promotion["expiration_date"]

        now = datetime.datetime.now().replace(tzinfo=expiration_date.tzinfo)

        if expiration_date < now:
            response = make_response("Promotion expired", 422)
            return abort(response)

        consumer_id = item["consumer_id"]

        if (
            _get_db().discounts.count(
                {"promotion_id": promotion_id, "consumer_id": consumer_id}
            )
            > 0
        ):
            response = make_response("Promotion already used", 422)
            return abort(response)

        discounts_count = _get_db().discounts.count({"promotion_id": promotion_id})

        if discounts_count >= promotion["discounts_quantity"]:
            response = make_response(
                "No more discounts available for this promotion", 422
            )
            return abort(response)


def add_consumer_id(items):
    for item in items:

        consumer_id = ObjectId(request.path.rsplit("/")[2])

        item["consumer_id"] = consumer_id


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

    # request was invalid
    if "_id" not in body:
        return

    discount_id = body["_id"]

    discount = _get_db().discounts.find_one({"_id": ObjectId(discount_id)})

    body["code"] = discount["code"]

    promotion_id = request.json["promotion_id"]

    promotion = _get_promotion(promotion_id)

    promotion["_id"] = str(promotion["_id"])
    promotion["expiration_date"] = _serialize_date(promotion["expiration_date"])

    body["expiration_date"] = promotion["expiration_date"]
    body["promotion"] = promotion

    payload.data = json.dumps(body)
