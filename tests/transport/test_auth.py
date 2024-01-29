import pytest

from httpx import AsyncClient

from gaming_progression_api.models.tokens import RecoveryToken, Token, VerifyToken
from gaming_progression_api.models.users import User
from gaming_progression_api.settings import Settings

token: str


@pytest.mark.asyncio
async def test_sign_up(
    client: AsyncClient,
    settings: Settings,
) -> None:
    response = await client.post(
        'auth/sign-up',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'full_name': 'string',
            'disabled': False,
            'password': 'string',
        },
    )
    assert response.status_code == 201

    response = await client.post(
        'auth/sign-up',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'full_name': 'string',
            'disabled': False,
            'password': 'string',
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_sign_in(
    client: AsyncClient,
) -> None:
    global token
    response = await client.post(
        'auth/sign-in',
        data={
            'username': 'string',
            'password': 'string',
        },
    )
    assert response.status_code == 200
    token = response.json()['access_token']
    assert Token.model_validate_json(response.text)


@pytest.mark.asyncio
async def test_users_me(
    client: AsyncClient,
) -> None:
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.get('auth/users/me', headers=headers)
    assert response.status_code == 200
    assert User.model_validate_json(response.text)


@pytest.mark.asyncio
async def test_users_me_patch(
    client: AsyncClient,
) -> None:
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.patch(
        'auth/users/me',
        headers=headers,
        json={
            'email': 'user@example2.com',
            'full_name': 'string2',
            'biography': 'string2',
            'birthdate': '2002-03-08',
            'password': 'string2',
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_verify_request(
    client: AsyncClient,
) -> None:
    global token
    response = await client.post(
        'auth/verify/request',
        json={
            'email': 'user@example2.com',
        },
    )
    token = response.json()['verify_token']
    assert response.status_code == 200
    assert VerifyToken.model_validate_json(response.text)


@pytest.mark.asyncio
async def test_verify(
    client: AsyncClient,
) -> None:
    response = await client.post('auth/verify', json={'token': token})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_password_recovery(
    client: AsyncClient,
) -> None:
    global token
    response = await client.post(
        'auth/password/recovery',
        json={
            'email': 'user@example2.com',
        },
    )
    token = response.json()['recovery_token']
    assert response.status_code == 200
    assert RecoveryToken.model_validate_json(response.text)


@pytest.mark.asyncio
async def test_password_reset(
    client: AsyncClient,
) -> None:
    global token

    response = await client.post('auth/password/reset', json={'token': token, 'password': 'string2'})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_verify_reset(
    client: AsyncClient,
) -> None:
    global token
    response = await client.post(
        'auth/sign-in',
        data={
            'username': 'string',
            'password': 'string2',
        },
    )
    assert Token.model_validate_json(response.text)
    assert response.status_code == 200

    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.patch(
        'auth/users/me',
        headers=headers,
        json={
            'email': 'user@example.com',
            'full_name': 'string2',
            'biography': 'string2',
            'birthdate': '2002-03-08',
            'password': 'string2',
        },
    )
    assert response.status_code == 200
