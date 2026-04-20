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

    assert result is None
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

    assert result is None
    assert session.query(Contract).count() == 0
