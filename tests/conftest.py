import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crm.models.base import Base
from crm.models.user import User
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.event import Event

from crm.repositories.user_repository import UserRepository
from crm.repositories.client_repository import ClientRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.event_repository import EventRepository

from crm.controllers.auth_controller import AuthController
from crm.controllers.user_controller import UserController
from crm.controllers.client_controller import ClientController
from crm.controllers.contract_controller import ContractController
from crm.controllers.event_controller import EventController


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture
def sales_payload():
    now = int(time.time())
    return {
        'sub': '1',
        'role': 'sales',
        'iat': now,
        'exp': now + 5000,
    }


@pytest.fixture
def management_payload():
    now = int(time.time())
    return {
        'sub': '2',
        'role': 'management',
        'iat': now,
        'exp': now + 5000,
    }


@pytest.fixture
def support_payload():
    now = int(time.time())
    return {
        'sub': '3',
        'role': 'support',
        'iat': now,
        'exp': now + 5000,
    }


@pytest.fixture
def user_repo(session):
    user_repo = UserRepository(session)
    return user_repo


@pytest.fixture
def auth_controller(session, user_repo):
    auth_controller = AuthController(session, user_repo)
    return auth_controller


@pytest.fixture
def user_controller(user_repo):
    user_controller = UserController(user_repo)
    return user_controller


@pytest.fixture
def user(session):
    user = User(
        email='employee-test@test.com',
        last_name='Un',
        first_name='Known',
        hashed_password='hashed123',
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
def client_controller(client_repo):
    client_controller = ClientController(client_repo)
    return client_controller


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
def contract_controller(contract_repo):
    contract_controller = ContractController(contract_repo)
    return contract_controller


@pytest.fixture
def contract_1(session, client_1):
    contract_1 = Contract(
        client_id=client_1.id
    )
    session.add(contract_1)
    session.commit()
    session.refresh(contract_1)
    return contract_1


@pytest.fixture
def contract_2(session, client_2):
    contract_2 = Contract(
        client_id=client_2.id
    )
    session.add(contract_2)
    session.commit()
    session.refresh(contract_2)
    return contract_2


@pytest.fixture
def event_repo(session):
    event_repo = EventRepository(session)
    return event_repo


@pytest.fixture
def event_controller(event_repo, contract_repo, user_repo):
    event_controller = EventController(event_repo, contract_repo, user_repo)
    return event_controller


@pytest.fixture
def event_1(session, contract_1):
    event_1 = Event(
        contract_id=contract_1.id,
    )
    session.add(event_1)
    session.commit()
    session.refresh(event_1)
    return event_1


@pytest.fixture
def event_2(session, contract_2):
    event_2 = Event(
        contract_id=contract_2.id,
    )
    session.add(event_2)
    session.commit()
    session.refresh(event_2)
    return event_2
