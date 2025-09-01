from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    level: int

class createUser(BaseUser):
    password: str

class login(BaseModel):
    username: str
    password: str
    
class getUser(BaseUser):
    id: int

    class config:
        from_attributes = True
