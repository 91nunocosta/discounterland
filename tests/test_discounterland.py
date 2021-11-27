from unittest.mock import MagicMock, patch

from discounterland import __version__
from discounterland.run import run


def test_version():
    assert __version__ == "0.1.0"


def test_run():
    app_mock = MagicMock()

    with patch("discounterland.run.create_app", return_value=app_mock):
        run()

        app_mock.run.assert_called()
