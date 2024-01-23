from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt

from gaming_progression_api.models.tokens import TokenData
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AuthService:
    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.using(rounds=15).hash(password)

    @classmethod
    async def create_access_token(cls, data: dict, expires_delta: timedelta | None = None):
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
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritm])
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
