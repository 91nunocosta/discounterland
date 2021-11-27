import random
import string
from bson import ObjectId
from flask import current_app, abort


def check_promotion(items):
    
    for item in items:
        promotion_id = item["promotion_id"]

        promotions = current_app.data.driver.db.promotions

        result = promotions.find_one({"_id": ObjectId(promotion_id)})

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
