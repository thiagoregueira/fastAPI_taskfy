from sqlalchemy import select

from fast_zero.models.models import User


def test_create_user(session):
    user = User(
        username='thiago',
        email='thiago@example.com',
        password='123456',
    )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'thiago@example.com')
    )

    assert result.id == 1
