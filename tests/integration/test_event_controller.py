from datetime import date

from crm.models.event import Event


# Test the method create_event

def test_create_event_returns_event_after_saving_in_database(
        monkeypatch,
        sales_payload,
        contract_1,
        event_controller,
        session
    ):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    contract_1.client.sales_contact_id = int(sales_payload['sub'])

    contract_1.signed = True

    result = event_controller.create_event(
        contract=contract_1,
        start_date=' 02/02/2022  ',
        end_date=None,
        support_contact_id=None,
        location='  new york',
        number_of_attendees='100',
        notes='  This is a note.   '
    )

    assert result is not None
    assert result.id is not None
    assert result.contract_id == contract_1.id
    assert result.start_date == date(2022, 2, 2)
    assert result.end_date is None
    assert result.support_contact_id is None
    assert result.location == 'new york'
    assert result.number_of_attendees == 100
    assert result.notes == 'This is a note.'

    saved_event = session.query(Event).filter(Event.id == result.id).first()
    
    assert saved_event is not None
    assert saved_event.contract_id == result.contract_id
    assert saved_event.start_date == result.start_date
    assert saved_event.end_date == result.end_date
    assert saved_event.support_contact_id == result.support_contact_id
    assert saved_event.location == result.location
    assert saved_event.number_of_attendees == result.number_of_attendees
    assert saved_event.notes == result.notes

def test_create_event_returns_none_if_user_is_not_authenticated(
        monkeypatch,
        contract_1,
        event_controller,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: None)
    
    result = event_controller.create_event(
        contract=contract_1,
    )

    assert result is None
    assert session.query(Event).count() == 0


def test_create_event_returns_none_if_user_is_not_client_sales_contact(
        monkeypatch,
        management_payload,
        contract_1,
        event_controller,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)
    
    monkeypatch.setattr('crm.controllers.event_controller.is_authenticated',
                        lambda payload: True)
    
    result = event_controller.create_event(
        contract=contract_1,
    )

    assert result is None
    assert session.query(Event).count() == 0


def test_create_event_returns_none_if_contract_is_not_signed(
        monkeypatch,
        sales_payload,
        contract_1,
        event_controller,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    monkeypatch.setattr('crm.controllers.event_controller.is_authenticated',
                        lambda payload: True)
    
    contract_1.client.sales_contact_id = int(sales_payload['sub'])

    result = event_controller.create_event(
        contract=contract_1,
    )

    assert result is None
    assert session.query(Event).count() == 0
