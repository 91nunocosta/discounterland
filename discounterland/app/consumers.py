import logging

from eve.auth import TokenAuth
from flask import current_app, request
from jwt.exceptions import InvalidTokenError

from discounterland.auth.tokens import check_token

LOGGER = logging.getLogger(__name__)


class ConsumerJWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        try:
            token_payload = check_token(token)
        except InvalidTokenError as err:
            LOGGER.warning(
                f"Consumer auth failed. Token {token} is invalid. {type(err).__name__}: {str(err)}"  # noqa
            )
            return False

        username = token_payload["sub"]

        self.set_request_auth_value(username)

        accounts = current_app.data.driver.db["accounts"]
        auth_account = accounts.find_one({"username": username})
        auth_consumer_id = str(auth_account["_id"])

        requested_consumer_id = request.path.rsplit("/")[2]

        if auth_consumer_id != requested_consumer_id:
            LOGGER.warning(
                f"Consumer auth failed. Consumer {auth_consumer_id}, with username {username} is not authorized to generate discounts for {requested_consumer_id}."  # noqa
            )
            return False

        return True
