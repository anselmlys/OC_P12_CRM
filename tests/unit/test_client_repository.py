import pytest
from sqlalchemy.exc import SQLAlchemyError

from crm.models.client import Client


# Test the method get_all

def test_get_all_returns_list_of_clients(client_repo, client_1, client_2):
    result = client_repo.get_all()

    assert len(result) == 2
    assert result[0].first_name == 'Jane'


def test_get_all_returns_empty_list_if_client_not_found(client_repo):
    result = client_repo.get_all()

    assert result == []


# Test the method get_by_id

def test_get_by_id_returns_a_client(client_repo, client_1, client_2):
    result = client_repo.get_by_id(client_id=2)

    assert result is not None
    assert result.id == client_2.id
    assert result.email == client_2.email

def test_get_by_id_returns_none_if_not_found(client_repo):
    result = client_repo.get_by_id(client_id=1)

    assert result is None


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


# Test the method update_client

def test_update_client_returns_client_after_modifications(client_repo, client_1, session):
    updates = {
        'last_name': 'Dooe',
        'first_name': 'Jaane',
    }

    result = client_repo.update_client(client_1.id, updates)

    assert result.last_name == 'Dooe'
    assert result.first_name == 'Jaane'
    assert result.email == 'test@test.com'

    updated_client = session.query(Client).filter(Client.email == 'test@test.com').first()

    assert updated_client.id == result.id
    assert updated_client.last_name == result.last_name


def test_update_client_returns_none_if_client_not_found(client_repo):
    updates = {
        'last_name': 'Dooe',
        'first_name': 'Jaane',
    }
    
    result = client_repo.update_client(1, updates)

    assert result is None


def test_update_client_raises_error_if_field_not_allowed(client_repo, client_1):
    updates = {
        'last_name': 'Dooe',
        'first_name': 'Jaane',
        'id': 4
    }

    with pytest.raises(ValueError):
        client_repo.update_client(client_1.id, updates)


# Test the method delete_client

def test_delete_client_returns_true_if_client_deleted(client_repo, client_1, session):
    result = client_repo.delete_client(client_1.id)
    client = session.query(Client).filter(Client.id == client_1.id).first()

    assert result is True
    assert client is None


def test_delete_client_returns_false_if_client_not_found(client_repo):
    result = client_repo.delete_client(1)

    assert result is False
