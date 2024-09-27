from app.core.exceptions import UserNotFoundException
from app.repository.user import UserRepository
from app.utils.id_from_token import get_user_id_from_token

ALGORITHM = "HS256"


async def get_current_user(token: str):
    user_id = get_user_id_from_token(token)
    user = await UserRepository.find_by_id(user_id)
    if not user:
        raise UserNotFoundException
    return user
