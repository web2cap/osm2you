from jose import jwt

from app.core.config import settings
from app.core.exceptions import InvalidTokenException, TokenVerificationFailedException

ALGORITHM = "HS256"


def get_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.ST_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise InvalidTokenException
        return user_id
    except jwt.JWTError as e:
        raise TokenVerificationFailedException() from e
