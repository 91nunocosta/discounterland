import datetime

import bson
import validators
from eve.io.mongo import Validator


class ExtendedValidator(Validator):
    def _validate_isfuture(self, isfuture, field, value):
        if value <= datetime.datetime.now():
            self._error(field, "Value must be a future date")

    def _validate_isurl(self, isurl, field, value):
        if not validators.url(value):
            self._error(field, "Value must be a url")

    def _validate_isid(self, isurl, field, value):
        if not bson.ObjectId.is_valid(value):
            self._error(field, "Value must be an id")
