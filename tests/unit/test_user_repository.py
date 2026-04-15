import pytest
from sqlalchemy.exc import SQLAlchemyError

from crm.models.user import User


# Test the method get_by_email

def test_get_by_email_returns_user(user_repo, user):
    result = user_repo.get_by_email('employee-test@test.com')

    assert result.email == 'employee-test@test.com'


def test_get_by_email_returns_none_if_user_not_found(user_repo):
    result = user_repo.get_by_email('unknown@test.com')

    assert result is None


# Test the method create_user

def test_create_user_returns_user_and_save_in_database(user_repo, session):
    result = user_repo.create_user(
        email = 'employee-test@test.com',
        last_name='Un',
        first_name='Known',
        hashed_password='hashed',
        role='sales'
    )

    assert result.id is not None
    assert result.email == 'employee-test@test.com'
    assert result.last_name == 'Un'
    assert result.first_name == 'Known'
    assert result.hashed_password == 'hashed'
    assert result.role == 'sales'

    saved_user = session.query(User).filter(User.email == 'employee-test@test.com').first()

    assert saved_user.id == result.id
    assert saved_user.email == result.email
    

def test_create_user_rolls_back_on_error(user_repo, session, monkeypatch):
    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    monkeypatch.setattr(session, 'commit', mock_commit)

    with pytest.raises(RuntimeError):
        user_repo.create_user(
            email = 'test@test.com',
            last_name='Doe',
            first_name='Jane',
            hashed_password='hashed',
            role='sales'
        )
