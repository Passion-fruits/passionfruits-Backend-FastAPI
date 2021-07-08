from pydantic import BaseModel, constr, EmailStr, conlist


class SignUp(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    user_genre: conlist(str, min_items=1, max_items=3)


class GoogleOauth(BaseModel):
    id_token: str
