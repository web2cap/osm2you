import pytest
from jose import jwt

from app.core.config import settings
from app.core.exceptions import InvalidTokenException, TokenVerificationFailedException
from app.utils.id_from_token import get_user_id_from_token


def test_get_user_id_from_token_valid():
    """Test extracting user ID from a valid token."""
    user_id = 5
    payload = {"user_id": user_id}
    token = jwt.encode(payload, settings.ST_SECRET_KEY, algorithm="HS256")

    result = get_user_id_from_token(token)

    assert result == user_id


def test_get_user_id_from_token_invalid_signature():
    """Test extracting user ID from a token with invalid signature."""
    payload = {"user_id": 5}
    token = jwt.encode(payload, "wrong_secret", algorithm="HS256")

    with pytest.raises(TokenVerificationFailedException):
        get_user_id_from_token(token)


def test_get_user_id_from_token_missing_user_id():
    """Test extracting user ID from a token missing the user_id claim."""
    payload = {"some_other_field": "value"}
    token = jwt.encode(payload, settings.ST_SECRET_KEY, algorithm="HS256")

    with pytest.raises(InvalidTokenException):
        get_user_id_from_token(token)


def test_get_user_id_from_token_malformed():
    """Test extracting user ID from a malformed token."""
    token = "not.a.token"

    with pytest.raises(TokenVerificationFailedException):
        get_user_id_from_token(token)
