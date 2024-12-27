from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='TesteDB', email='testedb@teste.com', password='TesteDB'
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(
        select(User).where(User.email == 'testedb@teste.com')
    )

    assert result.id == 1
