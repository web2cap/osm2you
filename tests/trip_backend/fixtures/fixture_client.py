import pytest
from app.main import app as fastapi_app
from httpx import ASGITransport, AsyncClient

TRANSPORT = ASGITransport(app=fastapi_app)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=TRANSPORT, base_url="https://test") as ac:
        yield ac
