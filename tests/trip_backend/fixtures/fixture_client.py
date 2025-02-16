import pytest
from app.core.config import settings
from app.main import app as fastapi_app
from httpx import ASGITransport, AsyncClient
from jose import jwt

TRANSPORT = ASGITransport(app=fastapi_app)
AUTHENTICATED_USER_ID = 2
NOT_OWNER_USER_ID =1


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=TRANSPORT, base_url="https://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(transport=TRANSPORT, base_url="https://test") as ac:
        token = create_jwt_for_user(AUTHENTICATED_USER_ID)
        ac.headers = {
            **ac.headers,
            "Authorization": f"Bearer {token}",
        }

        yield ac

@pytest.fixture(scope="session")
async def authenticated_not_owner_ac():
    async with AsyncClient(transport=TRANSPORT, base_url="https://test") as ac:
        token = create_jwt_for_user(NOT_OWNER_USER_ID)
        ac.headers = {
            **ac.headers,
            "Authorization": f"Bearer {token}",
        }

        yield ac


def create_jwt_for_user(user_id: int) -> str:
    """Helper function to create a JWT token."""
    payload = {"user_id": user_id}
    token = jwt.encode(payload, settings.ST_SECRET_KEY, algorithm="HS256")
    return token
