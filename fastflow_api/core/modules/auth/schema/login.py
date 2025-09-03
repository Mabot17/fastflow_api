from core.shared.base import StatusResponseSchema
from pydantic import BaseModel
from core.modules.users.schema.users_schema import UsersRespSchema


class LoginRespSchema(BaseModel):
    access_token: str
    token_type: str
    user: UsersRespSchema
    status: StatusResponseSchema
