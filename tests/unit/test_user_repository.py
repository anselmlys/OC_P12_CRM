import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from crm.models.base import Base
from crm.models.user import User
from crm.repositories.user_repository import UserRepository


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

@pytest.fixture
def user():
    return User(
        email='test@test.com',
        last_name='Doe',
        first_name='Jane',
        hashed_password='hashed',
        role='sales'
    )


# Test the method get_by_email

def test_get_by_email_returns_user(session, user):
    repo = UserRepository(session)

    session.add(user)
    session.commit()

    result = repo.get_by_email('test@test.com')

    assert result.email == 'test@test.com'


def test_get_by_email_returns_none_if_user_not_found(session):
    repo = UserRepository(session)

    result = repo.get_by_email('unknown@test.com')

    assert result is None


# Test the method create_user

def test_create_user_returns_user_and_save_in_database(session):
    repo = UserRepository(session)
    
    result = repo.create_user(
        email = 'test@test.com',
        last_name='Doe',
        first_name='Jane',
        hashed_password='hashed',
        role='sales'
    )

    assert result.id is not None
    assert result.email == 'test@test.com'
    assert result.last_name == 'Doe'
    assert result.first_name == 'Jane'
    assert result.hashed_password == 'hashed'
    assert result.role == 'sales'

    saved_user = session.query(User).filter(User.email == 'test@test.com').first()

    assert saved_user.id == result.id
    assert saved_user.email == result.email
    

def test_create_user_rolls_back_on_error(session, monkeypatch):
    repo = UserRepository(session)

    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    monkeypatch.setattr(session, 'commit', mock_commit)

    with pytest.raises(RuntimeError):
        repo.create_user(
            email = 'test@test.com',
            last_name='Doe',
            first_name='Jane',
            hashed_password='hashed',
            role='sales'
        )
