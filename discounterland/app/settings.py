import os

from discounterland.app.auth import JWTTokenAuth
from discounterland.app.consumers import ConsumerJWTTokenAuth
from discounterland.app.brands import BrandsJWTTokenAuth


SETTINGS = {
    "SERVER_NAME": os.environ.get("SERVER_NAME", "0.0.0.0:5000"),
    "MONGO_HOST": os.environ.get("MONGO_HOST", "localhost"),
    # The next setting disables concurrency control
    # (https://docs.python-eve.org/en/stable/features.html#concurrency).
    # Concurrency control ensures that two clients requesting a change to a same item
    # don't interfer with each other.
    # The clients must prove it knows the latest version of the item.
    # For that it needs to provide the correct etag (an hash).
    # The etag is returned by the server on each operation over the item.
    # I chose to disable this to make it easier to try out the API.
    # In a real-life scenario I would't do so.
    "DATE_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "IF_MATCH": False,
    "DOMAIN": {
        "accounts": {
            "resource_methods": ["POST"],
            "public_methods": ["POST"],
            "schema": {
                "username": {
                    "type": "string",
                    "required": True,
                    "unique": True,
                },
                "password": {
                    "type": "string",
                    "required": True,
                },
            },
        },
        "brands": {
            "resource_methods": [],
            "public_methods": [],
            "schema": {},
        },
        "consumers": {
            "resource_methods": [],
            "public_methods": [],
            "schema": {},
        },
        "promotions": {
            "authentication": BrandsJWTTokenAuth,
            "url": 'brands/<regex("[a-f0-9]{24}"):brand_id>/promotions',
            "resource_methods": ["POST"],
            "public_methods": [],
            "schema": {
                "brand_id": {
                    "type": "string",
                },
                "expiration_date": {
                    "type": "datetime",
                    "isfuture": True,
                },
                "product": {
                    "type": "dict",
                    "schema": {
                        "name": {"type": "string"},
                        "images": {
                            "type": "list",
                            "schema": {
                                "type": "string",
                            },
                        },
                    },
                },
                "discounts_quantity": {
                    "type": "integer",
                    "min": 1,
                },
            },
        },
        "discounts": {
            "authentication": ConsumerJWTTokenAuth,
            "url": 'consumers/<regex("[a-f0-9]{24}"):consumer_id>/discounts',
            "resource_methods": ["POST"],
            "public_methods": [],
            "schema": {
                "promotion_id": {
                    "type": "string",
                },
            },
        },
    },
}
