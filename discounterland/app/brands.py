from bson import ObjectId
from eve.auth import TokenAuth
from flask import current_app, request

from discounterland.auth.tokens import check_token


class BrandsJWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        token_payload = check_token(token)

        if token_payload is None:
            return False

        username = token_payload["sub"]

        self.set_request_auth_value(username)

        requested_brand_id = request.path.rsplit("/")[2]

        db = current_app.data.driver.db

        auth_account_id = db.accounts.find_one({"username": username})["_id"]

        result = db.brand_managers.find_one(
            {"account_id": auth_account_id, "brand_id": ObjectId(requested_brand_id)}
        )
        if result is None:
            return False

        return True
