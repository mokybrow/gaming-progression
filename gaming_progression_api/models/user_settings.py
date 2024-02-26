


from pydantic import UUID4, BaseModel


class MailingSettingsDTO(BaseModel):
    id: UUID4
    name: str
    code: int

class MailingSettingsResponseModel(BaseModel):
    user_id: UUID4
    type_data: MailingSettingsDTO 