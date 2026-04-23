import pytest
from sqlalchemy.exc import SQLAlchemyError

from crm.models.contract import Contract
from crm.repositories.contract_repository import ContractRepository


# Test the method create_contract

def test_create_contract_returns_contract_and_save_in_database(contract_repo, client_1, session):
    result = contract_repo.create_contract(
        client_id=client_1.id,
        total_amount=2000,
        signed=True,
    )

    assert result.id is not None
    assert result.client_id == client_1.id
    assert result.total_amount == 2000
    assert result.remaining_amount == None
    assert result.signed == True

    saved_contract = session.query(Contract).filter(Contract.client_id == client_1.id).first()

    assert saved_contract.id == result.id
    assert saved_contract.total_amount == 2000


def test_create_contract_rolls_back_on_error(contract_repo, client_1, session, monkeypatch):
    rollback_called = False

    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    def mock_rollback():
        nonlocal rollback_called
        rollback_called = True
    
    monkeypatch.setattr(session, 'commit', mock_commit)
    monkeypatch.setattr(session, 'rollback', mock_rollback)

    with pytest.raises(RuntimeError):
        contract_repo.create_contract(
            client_id=client_1.id,
            total_amount=2000,
            signed=True,
        )
    
    assert rollback_called is True


# Test the method get_unsigned_contracts

def test_get_unsigned_contracts_returns_list_of_contracts(
        contract_repo,
        contract_1,
        contract_2
):
    result = contract_repo.get_unsigned_contracts()

    assert len(result) == 2
    assert result[0] == contract_1


def test_get_unsigned_contracts_returns_empty_list_if_no_unsigned_contracts_found(
        contract_repo,
        contract_1,
        contract_2
):
    contract_1.signed = True
    contract_2.signed = True

    result = contract_repo.get_unsigned_contracts()

    assert result == []


# Test the method get_contracts_with_remaining_amounts

def test_get_contracts_with_remaining_amounts_returns_list_of_contracts(
        contract_repo,
        contract_1,
        contract_2
):
    contract_1.remaining_amount = 100
    contract_2.remaining_amount = 1

    result = contract_repo.get_contracts_with_remaining_amounts()

    assert len(result) == 2
    assert result[0] == contract_1


def test_get_contracts_with_remaining_amounts_returns_empty_list_if_no_contracts_found(
        contract_repo,
        contract_1,
        contract_2
):

    result = contract_repo.get_contracts_with_remaining_amounts()

    assert result == []
