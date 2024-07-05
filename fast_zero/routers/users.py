from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models.models import User
from fast_zero.schemas.user_schemas import (
    Message,
    UserListResponseSchema,
    UserResponseSchema,
    UserSchema,
)
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


# ----------CREATE USER-------------------------------------------------------
@router.post(
    '/',
    response_model=UserResponseSchema,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# ----------LIST USER----------------------------------------------------------
@router.get('/', response_model=UserListResponseSchema)
def list_users(
    session: T_Session,
    limit: int = 10,
    offset: int = 0,
):
    user = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': user}


# ----------UPDATE USER-------------------------------------------------------
@router.put('/{user_id}', response_model=UserResponseSchema)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only update your own user',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


# ----------DELETE USER-------------------------------------------------------
@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only delete your own user',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
