from pydantic import BaseModel


class GoogleOauth(BaseModel):
    id_token: str
