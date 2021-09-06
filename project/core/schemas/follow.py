from pydantic import BaseModel, conlist


class IsFollows(BaseModel):
    users: conlist(int, min_items=1)
