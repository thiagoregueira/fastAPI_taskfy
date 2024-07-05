from http import HTTPStatus

from fast_zero.schemas.user_schemas import UserResponseSchema


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'johndoe@example.com',
    }


def test_list_users_without_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_user(client, user):
    user_schema = UserResponseSchema.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Jane Doe',
            'email': 'janedoe@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Jane Doe',
        'email': 'janedoe@example.com',
    }


def test_update_wrong_user(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Jane Doe',
            'email': 'janedoe@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'You can only update your own user'}


# def test_update_user_not_found(client):
#     response = client.put(
#         '/users/2',
#         json={
#             'username': 'Jane Doe',
#             'email': 'janedoe@example.com',
#             'password': 'secret',
#         },
#     )
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'You can only delete your own user'}


# def test_delete_user_not_found(client):
#     response = client.delete('/users/2')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
