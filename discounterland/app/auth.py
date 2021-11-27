from typing import Any, Dict, Iterable

from eve.auth import TokenAuth
from flask import current_app, request

from discounterland.auth.passwords import check_password, password_hash
from discounterland.auth.tokens import check_token, generate_token


def replace_password_with_hash(items: Iterable[Dict[str, Any]]) -> None:
    """
    Replaces the password in a account item by a corresponding hash.
    """
    for account_item in items:
        password = account_item["password"]
        account_item["password"] = password_hash(password)


def login():
    db = current_app.data.driver.db

    payload = request.get_json()
    username = payload["username"]
    password = payload["password"]

    account = db.accounts.find_one({"username": username})

    if account is not None and check_password(password, account["password"]):
        response = {"token": generate_token(username)}
        return response, 200

    invalid_login_response = {
        "_status": "ERR",
        "_error": "Invalid username or password",
    }

    return invalid_login_response, 401


class JWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        token_payload = check_token(token)
        username = token_payload["sub"]
        self.set_request_auth_value(username)
        return token_payload is not None
