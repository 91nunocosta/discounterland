from eve import Eve

from discounterland.app.auth import login, replace_password_with_hash
from discounterland.app.discounts import (
    add_code,
    add_consumer_id,
    add_promotion_details,
    check_promotion,
)
from discounterland.app.settings import SETTINGS
from discounterland.app.validation import ExtendedValidator


def create_app():
    app = Eve(settings=SETTINGS, validator=ExtendedValidator)

    app.on_insert_accounts += replace_password_with_hash
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    app.on_insert_discounts += add_consumer_id
    app.on_insert_discounts += check_promotion
    app.on_insert_discounts += add_code
    app.on_post_POST_discounts += add_promotion_details

    return app
