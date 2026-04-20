import pytest

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

    assert result is None


# Test the method create_client

def test_create_client_returns_client_and_save_in_database(monkeypatch, sales_payload,
                                                     client_controller, session):
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


def test_create_client_returns_none_if_user_not_authenticated(monkeypatch, client_controller, session):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: None,)

    result = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    assert result is None
    assert session.query(Client).count() == 0


def test_create_client_returns_none_if_user_does_not_have_sales_role(client_controller, management_payload, session, monkeypatch):
    monkeypatch.setattr('crm.controllers.client_controller.get_current_user_payload',
                        lambda: management_payload,)
    
    monkeypatch.setattr('crm.controllers.client_controller.is_authenticated',
                        lambda payload: True,)

    result = client_controller.create_client(
        last_name='Doe',
        first_name='Jane',
        email='test@test.com'
    )

    assert result is None
    assert session.query(Client).count() == 0
