import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from crm.models.base import Base
from crm.models.contract import Contract
from crm.models.client import Client
from crm.repositories.contract_repository import ContractRepository

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

@pytest.fixture
def client(session):
    client = Client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@pytest.fixture
def contract_repo(session):
    contract_repo = ContractRepository(session)
    return contract_repo

@pytest.fixture
def contract_1(session, client):
    contract_1 = Contract(
        client_id = client.id
    )
    session.add(contract_1)
    session.commit()
    session.refresh(contract_1)
    return contract_1

@pytest.fixture
def contract_2(session, client):
    contract_2 = Contract(
        client_id = client.id
    )
    session.add(contract_2)
    session.commit()
    session.refresh(contract_2)
    return contract_2


# Test the method get_all

def test_get_all_returns_list_of_contracts(contract_repo, contract_1, contract_2):
    result = contract_repo.get_all()

    assert len(result) == 2
    assert result[0].client_id == 1


def test_get_all_returns_empty_list_if_contract_not_found(contract_repo):
    result = contract_repo.get_all()

    assert result == []
