from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4

from gaming_progression_api.dependencies import (
    UOWDep,
    access_token_expires,
    get_current_user,
    reset_token_expires,
    verify_token_expires,
)
from gaming_progression_api.models.tokens import RecoveryToken, Token, VerifyToken
from gaming_progression_api.models.users import BaseUser, ChangeUserPassword, PatchUser, User, UserCreate
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.users import UsersService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/sign-in', description='Выдача пользователю токена доступа')
async def login_for_access_token(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await UsersService().authenticate_user(uow, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = await AuthService().create_token(
        {'sub': user.username, 'aud': settings.auth_audience}, access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me', response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.post('/sign-up', description='Регистрация пользователя')
async def add_user(user: UserCreate, uow: UOWDep):
    user_id = await UsersService().add_user(uow, user)

    return user_id


@router.post('/verify/request', response_model=VerifyToken)
async def verify_user_request(uow: UOWDep, email: str = Body(..., embed=True)) -> VerifyToken:
    user = await UsersService().get_user(uow, email)
    verify_token = await AuthService().create_token(
        {'sub': str(user.id), 'aud': settings.verify_audience}, verify_token_expires
    )

    return VerifyToken(verify_token=verify_token, token_type='bearer')


@router.post('/verify')
async def verify_user(uow: UOWDep, token: str = Body(..., embed=True)) -> UUID4:
    verify_user = await AuthService().verify_user(uow, token.token)
    return verify_user


@router.post('/password/recovery', response_model=RecoveryToken)
async def password_recovery(uow: UOWDep, email: str = Body(..., embed=True)) -> RecoveryToken:
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User doesn't exist",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user = await UsersService().get_user(uow, email)
    if not user:
        raise credentials_exception
    recovery_token = await AuthService().create_token(
        {'sub': str(user.id), 'aud': settings.reset_audience}, reset_token_expires
    )

    return RecoveryToken(recovery_token=recovery_token, token_type='bearer')


@router.post('/password/reset')
async def password_reset(new_data: ChangeUserPassword, uow: UOWDep) -> UUID4:
    reset_user = await AuthService().reset_password(uow, new_data)
    return reset_user


@router.patch('/users/me')
async def password_reset(new_data: PatchUser, uow: UOWDep, current_user: Annotated[User, Depends(get_current_user)]):
    patch_user = await UsersService().edit_user(uow, current_user.id, new_data)
    if patch_user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Data changed successfully',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return patch_user
