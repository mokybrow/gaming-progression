import datetime
import uuid

from uuid import UUID
from sqlalchemy import func, text

from sqlalchemy.orm import Mapped, mapped_column

from gaming_progression_api.integrations.database import Base
from gaming_progression_api.models.users import User, UserCreate, UserSchema


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=True)
    biography: Mapped[str] = mapped_column(nullable=True)
    birthdate: Mapped[datetime.date] = mapped_column(nullable=True)
    disabled: Mapped[bool] = mapped_column(default=False)

    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_moderator: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            biography=self.biography,
            birthdate=self.birthdate,
            disabled=self.disabled,
            is_verified=self.is_verified,
            is_superuser=self.is_superuser,
            is_moderator=self.is_moderator,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
