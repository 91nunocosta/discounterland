from eve import Eve

from discounterland import __version__
from discounterland.app.auth import login, replace_password_with_hash
from discounterland.app.settings import SETTINGS

from discounterland.app.discounts import check_promotion

def create_app():
    from eve_swagger import get_swagger_blueprint

    swagger = get_swagger_blueprint()

    app = Eve(settings=SETTINGS)

    app.on_insert_accounts += replace_password_with_hash
    app.add_url_rule("/login", view_func=login, methods=["POST"])

    app.register_blueprint(swagger)

    app.config["SWAGGER_INFO"] = {
        "title": "Discounterland",
        "version": __version__,
        "description": "an API for generating discount codes",
        "contact": {"name": "Nuno Costa"},
        "schemes": ["http"],
    }

    app.on_insert_discounts += check_promotion

    return app
