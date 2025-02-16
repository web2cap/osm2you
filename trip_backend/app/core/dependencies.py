from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import IncativeUserException, UserNotFoundException
from app.repository.user import UserRepository
from app.utils.id_from_token import get_user_id_from_token

OAUTH2_SHEME =  OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Security(OAUTH2_SHEME)):
    """Extracts the user from the Bearer token in Authorization header."""
    user_id = get_user_id_from_token(token)
    user = await UserRepository.find_by_id(user_id)
    if not user:
        raise UserNotFoundException()
    if not user.is_active:
        raise IncativeUserException()
    return user
