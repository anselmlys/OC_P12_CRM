from datetime import date

from crm.models.event import Event


# Test the method get_events_to_assign

def test_get_events_to_assign_returns_list_of_events(
        event_controller,
        event_1,
        event_2,
        management_payload,
        monkeypatch
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)

    result = event_controller.get_events_to_assign()

    assert result is not None
    assert len(result) == 2
    assert result[0] == event_1


def test_get_events_to_assign_returns_none_if_user_not_authenticated(
        event_controller,
        event_1,
        event_2,
        monkeypatch
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: None)

    result = event_controller.get_events_to_assign()

    assert result == 'user_not_authenticated'


def test_get_events_to_assign_returns_none_if_user_does_have_management_role(
        event_controller,
        event_1,
        event_2,
        sales_payload,
        monkeypatch
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: sales_payload)

    result = event_controller.get_events_to_assign()

    assert result == 'user_not_management_role'


# Test the method get_assigned_events

def test_get_assigned_events_returns_list_of_events(
        event_controller,
        event_1,
        event_2,
        support_payload,
        monkeypatch
):
    event_1.support_contact_id = int(support_payload['sub'])
    event_2.support_contact_id = int(support_payload['sub'])

    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: support_payload)

    result = event_controller.get_assigned_events()

    assert len(result) == 2
    assert result[0] == event_1


def test_get_assigned_events_returns_none_if_user_not_authenticated(
        event_controller,
        event_1,
        event_2,
        support_payload,
        monkeypatch
):
    event_1.support_contact_id = int(support_payload['sub'])
    event_2.support_contact_id = int(support_payload['sub'])

    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: None)

    result = event_controller.get_assigned_events()

    assert result == 'user_not_authenticated'


def test_get_assigned_events_returns_none_if_user_does_not_have_support_role(
        event_controller,
        management_payload,
        monkeypatch
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)

    result = event_controller.get_assigned_events()

    assert result == 'user_not_support_role'


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
        contract_id=contract_1.id,
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
        contract_id=contract_1.id,
    )

    assert result == 'user_not_authenticated'
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
        contract_id=contract_1.id,
    )

    assert result == 'user_not_client_contact'
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
        contract_id=contract_1.id,
    )

    assert result == 'contract_not_signed'
    assert session.query(Event).count() == 0


# Test the method assign_support_contact

def test_assign_support_contact_returns_updated_event(
        monkeypatch,
        event_controller,
        event_1,
        management_payload,
        user
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)

    user.role = 'support'

    result = event_controller.assign_support_contact(event_1.id, user.id)

    assert result is not None
    assert result.support_contact_id == user.id


def test_assign_support_contact_returns_none_if_user_not_authenticated(
        monkeypatch,
        event_controller,
        event_1,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: None)

    result = event_controller.assign_support_contact(event_1.id, user.id)

    assert result == 'user_not_authenticated'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.support_contact_id is None


def test_assign_support_contact_returns_none_if_user_does_not_have_management_role(
        monkeypatch,
        event_controller,
        event_1,
        sales_payload,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: sales_payload)

    monkeypatch.setattr('crm.controllers.event_controller.is_authenticated',
                        lambda payload: True)

    result = event_controller.assign_support_contact(event_1.id, user.id)

    assert result == 'user_not_management_role'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.support_contact_id is None


def test_assign_support_contact_returns_none_if_support_contact_not_found(
        monkeypatch,
        event_controller,
        event_1,
        management_payload,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)

    monkeypatch.setattr('crm.controllers.event_controller.is_authenticated',
                        lambda payload: True)

    monkeypatch.setattr(
        event_controller.user_repository,
        'get_by_id',
        lambda support_contact_id: None
    )

    result = event_controller.assign_support_contact(event_1.id, user.id)

    assert result == 'support_contact_not_found'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.support_contact_id is None


def test_assign_support_contact_returns_none_if_user_for_contact_is_not_support(
        monkeypatch,
        event_controller,
        event_1,
        management_payload,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: management_payload)

    monkeypatch.setattr('crm.controllers.event_controller.is_authenticated',
                        lambda payload: True)

    result = event_controller.assign_support_contact(event_1.id, user.id)

    assert result == 'support_contact_not_support_role'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.support_contact_id is None


# Test the method update_event

def test_update_event_returns_updated_event_after_saving_in_database(
        monkeypatch,
        support_payload,
        event_1,
        event_controller,
        contract_2,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: support_payload)

    event_1.support_contact_id = int(support_payload['sub'])

    result = event_controller.update_event(
        event_1.id,
        start_date='02/02/2022',
        location=None,
        number_of_attendees='200',
        notes='   ',
    )

    assert result is not None
    assert result.start_date == date(2022, 2, 2)
    assert result.end_date is None
    assert result.location is None
    assert result.number_of_attendees == 200
    assert result.notes is None

    updated_event = session.query(Event).filter(Event.id == event_1.id).first()

    assert updated_event is not None
    assert updated_event.start_date == result.start_date


def test_update_event_returns_unchanged_event_if_update_none(
        monkeypatch,
        support_payload,
        event_1,
        event_controller,
        contract_2,
        session
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: support_payload)

    event_1.support_contact_id = int(support_payload['sub'])

    result = event_controller.update_event(
        event_1.id,
        start_date=None,
        location=None,
        number_of_attendees=None,
        notes=None,
    )

    assert result is not None
    assert result.start_date is None
    assert result.end_date is None
    assert result.location is None
    assert result.number_of_attendees is None
    assert result.notes is None

    updated_event = session.query(Event).filter(Event.id == event_1.id).first()

    assert updated_event is not None
    assert updated_event.start_date == result.start_date


def test_update_event_returns_none_if_user_not_authenticated(
        monkeypatch,
        session,
        event_controller,
        event_1
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: None)

    result = event_controller.update_event(
        event_1.id,
        start_date='02/02/2022',
    )

    assert result == 'user_not_authenticated'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.start_date is None


def test_update_event_returns_none_if_event_not_found(
        monkeypatch,
        session,
        support_payload,
        event_controller,
        event_1
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: support_payload)

    monkeypatch.setattr(event_controller.event_repository,
                        'get_by_id',
                        lambda id: None)

    result = event_controller.update_event(
        event_1.id,
        start_date='02/02/2022',
    )

    assert result == 'event_not_found'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.start_date is None


def test_update_event_returns_none_if_user_is_not_support_contact(
        monkeypatch,
        session,
        support_payload,
        event_controller,
        event_1
):
    monkeypatch.setattr('crm.controllers.event_controller.get_current_user_payload',
                        lambda: support_payload)

    result = event_controller.update_event(
        event_1.id,
        start_date='02/02/2022',
    )

    assert result == 'user_not_client_support_contact'

    event = session.query(Event).filter(Event.id == event_1.id).first()

    assert event is not None
    assert event.start_date is None
