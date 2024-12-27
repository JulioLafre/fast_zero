from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'user@example.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'user@example.com',
        'id': 1,
    }


def test_create_user_already_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Test',
            'email': 'anothertest@test.com',
            'password': 'anothertest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_already_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Test123',
            'email': 'test@test.com',
            'password': 'anothertest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_not_found(client, user):
    response = client.get('/users/100/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users_with_data(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1 ',
        json={
            'username': 'testeupdate',
            'email': 'update@example.com',
            'password': 'update',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'testeupdate',
        'email': 'update@example.com',
        'id': 1,
    }


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/100',
        json={
            'username': 'testenotfound',
            'email': 'teste@notfound.com',
            'password': 'notfound',
            'id': 100,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User has been deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/100/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
