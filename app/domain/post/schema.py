from pydantic import BaseModel


class BasePost(BaseModel):
    title: str
    content: str

class CreatePost(BasePost):
    user_id: int

class GetPost(BasePost):
    id: int
    user_id: int
    class Config:
        from_attributes = True
