import pytest

from httpx import AsyncClient

from gaming_progression_api.settings import Settings


@pytest.mark.asyncio
async def test_sign_up(
    client: AsyncClient,
    settings: Settings,
) -> None:
    response = await client.post(
        "auth/sign-up",
        json={
            "username": "string",
            "email": "user@example.com",
            "full_name": "string",
            "disabled": False,
            "password": "string",
        },
    )
    print(response.text)
    # assert response.status_code == 201
