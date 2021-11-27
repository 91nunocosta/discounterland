from bson import ObjectId
from flask import current_app, abort


def check_promotion(items):
    
    for item in items:
        promotion_id = item["promotion_id"]

        promotions = current_app.data.driver.db.promotions

        result = promotions.find_one({"_id": ObjectId(promotion_id)})

        if result is None:
            abort(422)
