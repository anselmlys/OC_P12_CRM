import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crm.models.base import Base
from crm.models.user import User
from crm.models.client import Client
from crm.models.contract import Contract
from crm.repositories.user_repository import UserRepository
from crm.repositories.client_repository import ClientRepository
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
def user_repo(session):
    user_repo = UserRepository(session)
    return user_repo


@pytest.fixture
def user(session):
    user = User(
        email='employee-test@test.com',
        last_name='Un',
        first_name='Known',
        hashed_password='hashed',
        role='sales'
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def client_repo(session):
    client_repo = ClientRepository(session)
    return client_repo


@pytest.fixture
def client_1(session):
    client_1 = Client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )
    session.add(client_1)
    session.commit()
    session.refresh(client_1)
    return client_1


@pytest.fixture
def client_2(session):
    client_2 = Client(
        last_name='Doe',
        first_name='John',
        email='test2@test.com'
    )
    session.add(client_2)
    session.commit()
    session.refresh(client_2)
    return client_2


@pytest.fixture
def contract_repo(session):
    contract_repo = ContractRepository(session)
    return contract_repo


@pytest.fixture
def contract_1(session, client_1):
    contract_1 = Contract(
        client_id = client_1.id
    )
    session.add(contract_1)
    session.commit()
    session.refresh(contract_1)
    return contract_1


@pytest.fixture
def contract_2(session, client_2):
    contract_2 = Contract(
        client_id = client_2.id
    )
    session.add(contract_2)
    session.commit()
    session.refresh(contract_2)
    return contract_2