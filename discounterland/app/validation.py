import datetime

import validators
from eve.io.mongo import Validator


class ExtendedValidator(Validator):
    def _validate_isfuture(self, isfuture, field, value):
        if not isfuture:
            return

        if value <= datetime.datetime.now():
            self._error(field, "Value must be a future date")

    def _validate_isurl(self, isurl, field, value):
        if not isurl:
            return

        if not validators.url(value):
            self._error(field, "Value must be a url")
