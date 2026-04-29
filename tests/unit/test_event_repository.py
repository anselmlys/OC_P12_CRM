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


# Test the method get_events_without_support_contact

def test_get_events_without_support_contact_returns_event_list(
        event_repo,
        event_1,
        event_2,
    ):

    result = event_repo.get_events_without_support_contact()

    assert len(result) == 2
    assert result[0] == event_1

def test_get_events_without_support_contact_returns_empty_list_if_no_event_found(
        event_repo,
        event_1,
        event_2,
        user
    ):

    event_1.support_contact_id = user.id
    event_2.support_contact_id = user.id

    result = event_repo.get_events_without_support_contact()

    assert result is not None
    assert result == []


# Test the method get_assigned_events

def test_get_events_by_support_contact_id_returns_list_of_events(
        user,
        event_repo,
        event_1,
        event_2,
):
    event_1.support_contact_id = user.id
    event_2.support_contact_id = user.id

    result = event_repo.get_events_by_support_contact_id(user.id)

    assert len(result) == 2
    assert result[0] == event_1


def test_get_events_by_support_contact_id_returns_empty_list_if_event_not_found(
        user,
        event_repo,
        event_1,
        event_2,
):
    result = event_repo.get_events_by_support_contact_id(user.id)

    assert result == []


# Test the method update_support_contact

def test_update_support_contact_returns_updated_event(event_repo, event_1,
                                                      user, session):
    result = event_repo.update_support_contact(event_1, user.id)

    assert result is not None
    assert result.support_contact_id == user.id

    updated_event = session.query(Event).filter(Event.id == result.id).first()

    assert updated_event is not None
    assert updated_event == result


def test_update_support_contact_rolls_back_on_error(
        monkeypatch,
        session,
        event_repo,
        event_1,
        user
    ):
    rollback_called = False
    
    def mock_commit():
        raise SQLAlchemyError('DB error')
    
    def mock_rollback():
        nonlocal rollback_called
        rollback_called = True
    
    monkeypatch.setattr(session, 'commit', mock_commit)
    monkeypatch.setattr(session, 'rollback', mock_rollback)

    with pytest.raises(RuntimeError):
        event_repo.update_support_contact(
            event_1,
            user.id
        )
    
    assert rollback_called is True
