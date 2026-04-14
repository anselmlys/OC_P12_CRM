import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from crm.models.base import Base
from crm.models.client import Client
from crm.repositories.client_repository import ClientRepository


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

@pytest.fixture
def client_1():
    return Client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

@pytest.fixture
def client_2():
    return Client(
        last_name='Doe',
        first_name='John',
        email='test2@test.com'
    )


# Test the method get_all

def test_get_all_returns_list_of_clients(session, client_1, client_2):
    repo = ClientRepository(session)

    session.add(client_1)
    session.add(client_2)
    session.commit()

    result = repo.get_all()

    assert len(result) == 2
    assert result[0].first_name == 'Jane'


def test_get_all_returns_empty_list_if_client_not_found(session):
    repo = ClientRepository(session)

    result = repo.get_all()

    assert result == []
