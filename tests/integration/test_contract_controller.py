import pytest

from crm.models.contract import Contract


# Test the method create_contract

def test_create_contract_returns_contract_after_saving_in_database(
        management_payload,
        monkeypatch,
        contract_controller,
        client_1,
        session
    ):

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = contract_controller.create_contract(
        client_id=str(client_1.id),
        total_amount=' 20000  ',
        signed=' yes ',
    )

    assert result.id is not None
    assert result.client_id == client_1.id
    assert result.total_amount == 20000
    assert result.remaining_amount is None
    assert result.signed is True

    saved_contract = session.query(Contract).filter(Contract.id == result.id).first()

    assert saved_contract is not None
    assert saved_contract.client_id == result.client_id
    assert saved_contract.total_amount == result.total_amount
    assert saved_contract.remaining_amount == result.remaining_amount
    assert saved_contract.signed == result.signed


def test_create_contract_returns_none_if_user_not_authenticated(
        monkeypatch,
        contract_controller,
        client_1,
        session
    ):

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: None)
    
    result = contract_controller.create_contract(
        client_id=str(client_1.id),
        total_amount=' 20000  ',
        signed=' yes ',
    )

    assert result == 'user_not_authenticated'
    assert session.query(Contract).count() == 0


def test_create_contract_returns_none_if_user_does_not_have_management_role(
        monkeypatch,
        contract_controller,
        client_1,
        session,
        sales_payload
    ):

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    monkeypatch.setattr('crm.controllers.contract_controller.is_authenticated',
                        lambda payload: True,)
    
    result = contract_controller.create_contract(
        client_id=str(client_1.id),
        total_amount=' 20000  ',
        signed=' yes ',
    )

    assert result == 'user_not_management_role'
    assert session.query(Contract).count() == 0


# Test the method get_unsigned_contracts

def test_get_unsigned_contracts_returns_list_of_contracts(
        monkeypatch,
        sales_payload,
        contract_1,
        contract_2,
        contract_controller
):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    result = contract_controller.get_unsigned_contracts()

    assert len(result) == 2
    assert result[0] == contract_1


def test_get_unsigned_contracts_returns_none_if_user_not_authenticated(
        monkeypatch,
        contract_1,
        contract_2,
        contract_controller
):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: None)
    
    result = contract_controller.get_unsigned_contracts()

    assert result == 'user_not_authenticated'


def test_get_unsigned_contracts_returns_none_if_user_does_not_have_sales_role(
        monkeypatch,
        management_payload,
        contract_1,
        contract_2,
        contract_controller
):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = contract_controller.get_unsigned_contracts()

    assert result == 'user_not_sales_role'


# Test the method get_unpaid_contracts

def test_get_unpaid_contracts_returns_list_of_contracts(
        monkeypatch,
        sales_payload,
        contract_1,
        contract_2,
        contract_controller
):
    contract_1.remaining_amount = 1000
    contract_2.remaining_amount = 1

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    result = contract_controller.get_unpaid_contracts()

    assert len(result) == 2
    assert result[0] == contract_1


def test_get_unpaid_contracts_returns_none_if_user_not_authenticated(
        monkeypatch,
        contract_1,
        contract_2,
        contract_controller
):
    contract_1.remaining_amount = 1000
    contract_2.remaining_amount = 1

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: None)
    
    result = contract_controller.get_unpaid_contracts()

    assert result == 'user_not_authenticated'


def test_get_unpaid_contracts_returns_none_if_user_does_not_have_sales_role(
        monkeypatch,
        management_payload,
        contract_1,
        contract_2,
        contract_controller
):
    contract_1.remaining_amount = 1000
    contract_2.remaining_amount = 1

    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = contract_controller.get_unpaid_contracts()

    assert result == 'user_not_sales_role'


# Test the method update_contract

def test_update_contract_returns_updated_contract_if_user_has_management_role(
        monkeypatch,
        management_payload,
        contract_controller,
        contract_1,
        client_2,
        session
    ):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = contract_controller.update_contract(
        contract_id=contract_1.id,
        client_id=str(client_2.id),
        total_amount='2000',
        remaining_amount=None,
        signed='yes',
    )

    assert result is not None
    assert result.client_id == client_2.id
    assert result.total_amount == 2000
    assert result.remaining_amount == None
    assert result.signed == True

    updated_contract = session.query(Contract).filter(Contract.id == contract_1.id).first()

    assert updated_contract is not None
    assert updated_contract.client_id == result.client_id
    assert updated_contract.total_amount == result.total_amount
    assert updated_contract.remaining_amount == result.remaining_amount
    assert updated_contract.signed == result.signed


def test_update_contract_returns_updated_contract_if_user_is_client_contact(
        monkeypatch,
        sales_payload,
        contract_controller,
        contract_1,
        client_1,
        session
    ):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    contract_1.client.sales_contact_id = int(sales_payload['sub'])

    result = contract_controller.update_contract(
        contract_id=contract_1.id,
        client_id=str(client_1.id),
        total_amount='2000',
        remaining_amount=None,
        signed='yes',
    )

    assert result is not None
    assert result.client_id == client_1.id
    assert result.total_amount == 2000
    assert result.remaining_amount == None
    assert result.signed == True

    updated_contract = session.query(Contract).filter(Contract.id == contract_1.id).first()

    assert updated_contract is not None
    assert updated_contract.client_id == result.client_id
    assert updated_contract.total_amount == result.total_amount
    assert updated_contract.remaining_amount == result.remaining_amount
    assert updated_contract.signed == result.signed


def test_update_contract_returns_none_if_user_is_not_authenticated(
        monkeypatch,
        contract_controller,
        contract_1,
        client_1,
        session
    ):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: None)
    
    result = contract_controller.update_contract(
        contract_id=contract_1.id,
        client_id=str(client_1.id),
        total_amount='2000',
    )

    assert result == 'user_not_authenticated'

    contract_in_db = session.query(Contract).filter(Contract.id == contract_1.id).first()

    assert contract_in_db.total_amount is None


def test_update_contract_returns_none_if_user_does_not_have_management_role_or_is_not_client_contact(
        monkeypatch,
        sales_payload,
        contract_controller,
        contract_1,
        client_1,
        session
    ):
    monkeypatch.setattr('crm.controllers.contract_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    monkeypatch.setattr('crm.controllers.contract_controller.is_authenticated',
                        lambda payload: True)
    
    result = contract_controller.update_contract(
        contract_id=contract_1.id,
        client_id=str(client_1.id),
        total_amount='2000',
    )

    assert result == 'user_not_client_contact'

    contract_in_db = session.query(Contract).filter(Contract.id == contract_1.id).first()

    assert contract_in_db.total_amount is None
