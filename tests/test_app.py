from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo'}


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'test',
                'email': 'user@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User has been deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_not_found(client):
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
