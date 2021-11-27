from unittest.mock import MagicMock, patch

from discounterland.auth.passwords import check_password, password_hash


def test_password_hash():
    password = "unsecurepassword"
    fake_hash = "fake_hash"
    fake_salt = "fake_salt"

    hashpw_mock = MagicMock(return_value=fake_hash)

    with patch("discounterland.auth.passwords.hashpw", hashpw_mock):
        with patch("discounterland.auth.passwords.gensalt", return_value=fake_salt):

            pw_hash = password_hash(password)

    hashpw_mock.assert_called_with(b"unsecurepassword", fake_salt)

    assert pw_hash == fake_hash


def test_valid_check_password():
    password = "unsecurepassword"
    fake_hash = b"fake_hash"

    checkpw_mock = MagicMock(return_value=True)

    with patch("discounterland.auth.passwords.checkpw", checkpw_mock):

        result = check_password(password, fake_hash)

    checkpw_mock.assert_called_with(b"unsecurepassword", fake_hash)

    assert result is True
