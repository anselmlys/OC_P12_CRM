import pytest
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from crm.models.event import Event


# Test the method create_event

def test_create_event_returns_event_and_save_in_database(event_repo, contract_1, session):
    result = event_repo.create_event(
        contract_id=contract_1.id,
        start_date=date(2026, 12, 9),
        number_of_attendees=50,
    )

    assert result.id is not None
    assert result.contract_id == contract_1.id
    assert result.start_date == date(2026, 12, 9)
    assert result.location == None
    assert result.number_of_attendees == 50

    saved_event = session.query(Event).filter(Event.contract_id==contract_1.id).first()

    assert saved_event.id == result.id
    assert saved_event.start_date == date(2026, 12, 9)


def test_create_event_rolls_back_on_error(event_repo, contract_1, session, monkeypatch):
    rollback_called = False

    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    def mock_rollback():
        nonlocal rollback_called
        rollback_called = True

    monkeypatch.setattr(session, 'commit', mock_commit)
    monkeypatch.setattr(session, 'rollback', mock_rollback)

    with pytest.raises(RuntimeError):
        event_repo.create_event(
            contract_id=contract_1.id,
            start_date=date(2026, 12, 9),
            number_of_attendees=50,
        )
    
    assert rollback_called is True
