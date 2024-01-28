from pydantic import BaseModel


class ServiceResponseModel(BaseModel):
    details: str
