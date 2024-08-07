from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from gaming_progression_api.dependencies import (
    UOWDep,
    access_token_expires,
    get_current_user,
    reset_token_expires,
    verify_token_expires,
)
from gaming_progression_api.models.service import ServiceResponseModel
from gaming_progression_api.models.tokens import RecoveryToken, Token, VerifyToken
from gaming_progression_api.models.users import ChangeUserPassword, PatchUser, User, UserCreate
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.users import UsersService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/sign-in', description='Выдача пользователю токена доступа', response_model=Token)
async def login_for_access_token(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await UsersService().authenticate_user(uow, form_data.username, form_data.password)
    return user

@router.post('/sign-up', description='Регистрация пользователя', response_model=Token)
async def add_user(user: UserCreate, uow: UOWDep) -> Token:
    result = await UsersService().add_user(uow, user)
    return result

@router.get('/users/me', response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.post('/verify/request', response_model=VerifyToken)
async def verify_user_request(uow: UOWDep, email: str = Body(..., embed=True)) -> VerifyToken:
    user = await UsersService().get_user_for_verify(uow, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already verified or incorrect email',
        )
    verify_token = await AuthService().create_token(
        {'sub': str(user.id), 'aud': settings.verify_audience},
        verify_token_expires,
    )

    return VerifyToken(verify_token=verify_token, token_type='bearer')


@router.post('/verify', response_model=ServiceResponseModel)
async def verify_user(uow: UOWDep, token: str = Body(..., embed=True)) -> ServiceResponseModel:
    verified_user = await AuthService().verify_user(uow, token)
    return ServiceResponseModel(details=f'user with id {verified_user} has been successfully verified')


@router.post('/change/email/request', response_model=VerifyToken)
async def verify_user_request(
    uow: UOWDep, current_user: Annotated[User, Depends(get_current_user)], email: str = Body(..., embed=True)
) -> VerifyToken:
    verify_token = await AuthService().create_token(
        {'sub': str(current_user.id), 'email': email, 'aud': settings.verify_audience},
        verify_token_expires,
    )
    await UsersService().change_user_email(uow, current_user.id, current_user.email, email, verify_token)
    return VerifyToken(verify_token=verify_token, token_type='bearer')


@router.post('/change/email', response_model=ServiceResponseModel)
async def verify_user(uow: UOWDep, token: str = Body(..., embed=True)) -> ServiceResponseModel:
    await AuthService().change_email(uow, token)
    return ServiceResponseModel(details=f'Email has been successfully changed')


@router.post('/change/password/request', response_model=VerifyToken)
async def verify_user_request(uow: UOWDep, current_user: Annotated[User, Depends(get_current_user)]) -> VerifyToken:
    verify_token = await AuthService().create_token(
        {'sub': str(current_user.id), 'aud': settings.reset_audience},
        reset_token_expires,
    )
    await UsersService().change_user_password(uow, current_user.id, current_user.email, verify_token)

    return VerifyToken(verify_token=verify_token, token_type='bearer')


@router.post('/password/recovery', response_model=RecoveryToken)
async def password_recovery(uow: UOWDep, email: str = Body(..., embed=True)) -> RecoveryToken:
    user = await UsersService().get_user(uow, email)

    recovery_token = await AuthService().create_token(
        {'sub': str(user.id), 'aud': settings.reset_audience},
        reset_token_expires,
    )

    return RecoveryToken(recovery_token=recovery_token, token_type='bearer')


@router.post(
    '/password/reset',
    response_model=ServiceResponseModel,
    description='To reset your password, you must send a reset token and a new password',
)
async def password_reset(new_data: ChangeUserPassword, uow: UOWDep) -> ServiceResponseModel:
    reset_user = await AuthService().reset_password(uow, new_data)
    return ServiceResponseModel(details=f'Password for {reset_user} successfully changed')


@router.patch('/users/me')
async def edit_user(
    new_data: PatchUser,
    uow: UOWDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ServiceResponseModel:
    patch_user = await UsersService().patch_user(uow, current_user.id, new_data)
    if patch_user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Data changed successfully',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return patch_user
