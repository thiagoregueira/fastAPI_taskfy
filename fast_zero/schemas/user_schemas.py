from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserListResponseSchema(BaseModel):
    users: list[UserResponseSchema]
