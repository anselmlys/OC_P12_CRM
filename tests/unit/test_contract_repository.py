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
