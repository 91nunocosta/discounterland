from eve.auth import TokenAuth
from flask import current_app, request
from jwt.exceptions import InvalidTokenError

from discounterland.auth.tokens import check_token


class ConsumerJWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        try:
            token_payload = check_token(token)
        except InvalidTokenError:
            return False

        username = token_payload["sub"]

        self.set_request_auth_value(username)

        accounts = current_app.data.driver.db["accounts"]
        auth_account = accounts.find_one({"username": username})
        auth_consumer_id = str(auth_account["_id"])

        requested_consumer_id = request.path.rsplit("/")[2]

        if auth_consumer_id != requested_consumer_id:
            return False

        return True
