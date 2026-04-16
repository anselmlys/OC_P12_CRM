import pytest
from sqlalchemy.exc import SQLAlchemyError

from crm.models.client import Client


# Test the method create_client

def test_create_client_returns_client_and_save_in_database(client_repo, session):
    result = client_repo.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com',
    )

    assert result.id is not None
    assert result.last_name == 'Doe'
    assert result.first_name == 'Jane'

    saved_client = session.query(Client).filter(Client.email == 'test@test.com').first()

    assert saved_client.id == result.id
    assert saved_client.email == result.email


def test_create_client_rolls_back_on_error(client_repo, session, monkeypatch):
    rollback_called = False
    
    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    def mock_rollback():
        nonlocal rollback_called
        rollback_called = True
    
    monkeypatch.setattr(session, 'commit', mock_commit)
    monkeypatch.setattr(session, 'rollback', mock_rollback)

    with pytest.raises(RuntimeError):
        client_repo.create_client(
            last_name='Doe',
            first_name='Jane',
            email='test@test.com',
        )
    
    assert rollback_called is True
