import os

from typing import Any, List, Optional, Dict

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr, Field
from starlette.responses import JSONResponse

from gaming_progression_api.settings import get_settings


settings = get_settings()


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=587,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME='mbrw support',
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER='./templates/email',
)


class EmailSchema(BaseModel):
    email: List[EmailStr] = Field(...)
    subject: str = Field(...)
    body: Dict[str, str] = Field(...)


async def email_sender(data: EmailSchema, template_name: str) -> JSONResponse:
    data = EmailSchema.model_validate(data)
    message = MessageSchema(
        subject=data.subject,
        recipients=data.model_dump().get("email"),
        template_body=data.model_dump().get("body"),
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)

    return JSONResponse(status_code=200, content={"message": "Reset email has been sent"})
