from eve.io.mongo import Validator
import datetime


class ExtendedValidator(Validator):

    def _validate_isfuture(self, isfuture, field, value):
        if not isfuture:
            return

        if value <= datetime.datetime.now():
            self._error(field, "Value must be a future date")
