from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas.user_schemas import (
    Message,
    UserDB,
    UserListResponseSchema,
    UserResponseSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/users/',
    response_model=UserResponseSchema,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', response_model=UserListResponseSchema)
def list_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserResponseSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}
