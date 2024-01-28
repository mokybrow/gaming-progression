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
    assert response.status_code == 201

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
    assert response.status_code == 400


token = "a"


@pytest.mark.asyncio
async def test_sign_in(
    client: AsyncClient,
    settings: Settings,
) -> None:
    global token
    response = await client.post(
        "auth/sign-in",
        data={
            "username": "string",
            "password": "string",
        },
    )
    assert response.status_code == 200
    print(response.json()['access_token'])
    token = response.json()['access_token']


@pytest.mark.asyncio
async def test_users_me(
    client: AsyncClient,
    settings: Settings,
) -> None:
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.get("auth/users/me", headers=headers)
    assert response.status_code == 200
    print(response.text)
