from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt

from gaming_progression_api.models.tokens import TokenData
from gaming_progression_api.models.users import ChangeUserPassword
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class AuthService:
    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.using(rounds=15).hash(password)

    @classmethod
    async def create_token(cls, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algoritm)
        return encoded_jwt

    async def get_current_user(self, uow: IUnitOfWork, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algoritm], audience=settings.auth_audience
            )
            username: str = payload.get('sub')
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as exc:
            raise credentials_exception from exc
        async with uow:
            user = await uow.users.find_one(username=token_data.username)

        if user is None:
            raise credentials_exception
        return user

    async def verify_user(self, uow: IUnitOfWork, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algoritm], audience=settings.verify_audience
            )
            id: str = payload.get('sub')
            if id is None:
                raise credentials_exception
            token_data = TokenData(id=id)
        except JWTError as exc:
            raise credentials_exception from exc

        async with uow:
            user = await uow.users.edit_one(token_data.id, {"disabled": True})
            await uow.commit()

        if user is None:
            raise credentials_exception
        return user

    async def reset_password(self, uow: IUnitOfWork, new_data: ChangeUserPassword):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                new_data.token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algoritm],
                audience=settings.reset_audience,
            )
            id: str = payload.get('sub')
            if id is None:
                raise credentials_exception
            token_data = TokenData(id=id)
        except JWTError as exc:
            raise credentials_exception from exc

        async with uow:
            user = await uow.users.edit_one(token_data.id, {"password": await self.hash_password(new_data.password)})
            await uow.commit()

        if user is None:
            raise credentials_exception
        return user
