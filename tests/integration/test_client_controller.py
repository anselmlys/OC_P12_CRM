from crm.models.client import Client


# Test the method get_all_clients

def test_get_all_clients_returns_list_of_clients(sales_payload, monkeypatch,
                                                 client_controller, client_1,
                                                 client_2):
    monkeypatch.setattr(
        'crm.controllers.client_controller.get_current_user_payload',
        lambda: sales_payload
    )

    result = client_controller.get_all_clients()

    assert result is not None
    assert len(result) == 2
    assert result[0].id == client_1.id
    assert result[1].id == client_2.id


def test_get_all_clients_returns_none_if_user_not_authenticated(monkeypatch, client_controller):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: None,)

    result = client_controller.get_all_clients()

    assert result == 'user_not_authenticated'


# Test the method create_client

def test_create_client_returns_client_and_save_in_database(
        monkeypatch, sales_payload, client_controller, session):
    monkeypatch.setattr(
        'crm.controllers.client_controller.get_current_user_payload',
        lambda: sales_payload
    )

    result = client_controller.create_client(
        last_name='   Doe ',
        first_name=' Jane   ',
        email=' TEST@TesT.COM  ',
        phone_number=' 0202020202  ',
    )

    assert result.id is not None
    assert result.last_name == 'Doe'
    assert result.first_name == 'Jane'
    assert result.email == 'test@test.com'
    assert result.phone_number == '0202020202'
    assert result.company_name is None
    assert result.sales_contact_id == int(sales_payload['sub'])

    saved_client = session.query(Client).filter(Client.id == result.id).first()

    assert saved_client is not None
    assert saved_client.last_name == 'Doe'
    assert saved_client.first_name == 'Jane'
    assert saved_client.email == 'test@test.com'
    assert saved_client.phone_number == '0202020202'
    assert result.company_name is None
    assert saved_client.sales_contact_id == int(sales_payload['sub'])


def test_create_client_returns_none_if_user_not_authenticated(
        monkeypatch, client_controller, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: None,)

    result = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    assert result == 'user_not_authenticated'
    assert session.query(Client).count() == 0


def test_create_client_returns_none_if_user_does_not_have_sales_role(
        client_controller, management_payload, session, monkeypatch):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: management_payload,)

    monkeypatch.setattr('crm.controllers.client_controller.is_authenticated',
                        lambda payload: True,)

    result = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    assert result == 'user_not_sales_role'
    assert session.query(Client).count() == 0


# Test the method update_client

def test_update_client_returns_updated_client_and_save_in_database(
        client_controller, sales_payload, monkeypatch, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: sales_payload,)

    client = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    result = client_controller.update_client(
        client_id=client.id,
        last_name='Doe',
        first_name='Jane',
        email=' janedoe@test.com   ',
        phone_number=' 0202020202   ',
        company_name=None,
    )

    assert result.last_name == 'Doe'
    assert result.first_name == 'Jane'
    assert result.email == 'janedoe@test.com'
    assert result.phone_number == '0202020202'
    assert result.company_name is None

    updated_client = session.query(Client).filter(Client.id == client.id).first()

    assert updated_client is not None
    assert updated_client.last_name == result.last_name
    assert updated_client.first_name == result.first_name
    assert updated_client.email == result.email
    assert updated_client.phone_number == result.phone_number
    assert updated_client.company_name == result.company_name


def test_update_client_returns_unchanged_client_if_update_none(
        client_controller, client_1, sales_payload, monkeypatch, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: sales_payload,)

    client_1.sales_contact_id = int(sales_payload['sub'])

    result = client_controller.update_client(
        client_id=client_1.id,
        last_name=None,
        first_name=None,
        email=None,
        phone_number=None,
        company_name=None,
    )

    assert result.last_name == 'Doe'
    assert result.first_name == 'Jane'
    assert result.email == 'test@test.com'
    assert result.phone_number is None
    assert result.company_name is None

    updated_client = session.query(Client).filter(Client.id == client_1.id).first()

    assert updated_client is not None
    assert updated_client.last_name == result.last_name
    assert updated_client.first_name == result.first_name
    assert updated_client.email == result.email
    assert updated_client.phone_number == result.phone_number
    assert updated_client.company_name == result.company_name


def test_update_client_returns_none_if_user_not_authenticated(
        monkeypatch, client_controller, sales_payload, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: sales_payload,)

    client = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: None,)

    result = client_controller.update_client(
        client_id=client.id,
        last_name='Doe',
        first_name='Jane',
        email=' janedoe@test.com   ',
        phone_number=' 0202020202   ',
        company_name=None,
    )

    assert result == 'user_not_authenticated'

    client_in_db = session.query(Client).filter(Client.id == client.id).first()

    assert client.email == client_in_db.email


def test_update_client_returns_none_if_user_does_not_have_sales_role(
        monkeypatch, client_controller, sales_payload, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: sales_payload,)

    client = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    sales_payload['role'] = 'management'

    result = client_controller.update_client(
        client_id=client.id,
        last_name='Doe',
        first_name='Jane',
        email=' janedoe@test.com   ',
        phone_number=' 0202020202   ',
        company_name=None,
    )

    assert result == 'user_not_sales_role'

    client_in_db = session.query(Client).filter(Client.id == client.id).first()

    assert client.email == client_in_db.email


def test_update_client_returns_none_if_user_not_contact_of_client(
        monkeypatch, client_controller, sales_payload, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: sales_payload,)

    client = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    sales_payload['sub'] = '2'

    result = client_controller.update_client(
        client_id=client.id,
        last_name='Doe',
        first_name='Jane',
        email=' janedoe@test.com   ',
        phone_number=' 0202020202   ',
        company_name=None,
    )

    assert result == 'user_not_client_contact'

    client_in_db = session.query(Client).filter(Client.id == client.id).first()

    assert client.email == client_in_db.email
