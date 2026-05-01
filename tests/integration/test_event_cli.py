from click.testing import CliRunner

from crm.cli.event_cli import events


# Test the command create

def test_create_event_displays_success(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def create_event(self, contract_id, start_date, end_date, support_contact_id,
                         location, number_of_attendees, notes):
            return True

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'create',
            '--contract-id', '1',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'Event successfully created.' in result.output


def test_create_event_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def create_event(self, contract_id, start_date, end_date, support_contact_id,
                         location, number_of_attendees, notes):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'create',
            '--contract-id', '1',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_create_event_displays_error_if_contract_not_found(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def create_event(self, contract_id, start_date, end_date, support_contact_id,
                         location, number_of_attendees, notes):
            return 'contract_not_found'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'create',
            '--contract-id', '1',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'The contract was not found.' in result.output


def test_create_event_displays_error_if_user_not_client_contact(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def create_event(self, contract_id, start_date, end_date, support_contact_id,
                         location, number_of_attendees, notes):
            return 'user_not_client_contact'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'create',
            '--contract-id', '1',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'You are not the contact of this client.' in result.output


def test_create_event_displays_error_if_contract_not_signed(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def create_event(self, contract_id, start_date, end_date, support_contact_id,
                         location, number_of_attendees, notes):
            return 'contract_not_signed'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'create',
            '--contract-id', '1',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'The contract is not signed yet.' in result.output


# Test the command list

def test_get_events_displays_list_of_events(monkeypatch):
    class FakeClient:
        id = 3
        first_name = 'Un'
        last_name = 'Known'

    class FakeContract:
        id = 2
        client = FakeClient()

    class FakeSupport:
        id = 4
        first_name = 'john'
        last_name = 'doe'

    class FakeEvent:
        def __init__(self):
            self.id = 1
            self.contract = FakeContract()
            self.support_contact_id = 4
            self.support_contact = FakeSupport()

    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_all_events(self):
            return [FakeEvent(),]

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert '3' in result.output
    assert 'Un Known' in result.output
    assert '2' in result.output
    assert '4' in result.output
    assert 'John Doe' in result.output


def test_get_events_displays_list_of_events_to_assign(monkeypatch):
    class FakeClient:
        id = 3
        first_name = 'Un'
        last_name = 'Known'

    class FakeContract:
        id = 2
        client = FakeClient()

    class FakeEvent:
        def __init__(self):
            self.id = 1
            self.contract = FakeContract()
            self.support_contact_id = None
            self.support_contact = None

    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_events_to_assign(self):
            return [FakeEvent(),]

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list', '--to-assign'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert '3' in result.output
    assert 'Un Known' in result.output
    assert '2' in result.output
    assert '-' in result.output


def test_get_events_displays_list_of_events_assigned_to_user(monkeypatch):
    class FakeClient:
        id = 3
        first_name = 'Un'
        last_name = 'Known'

    class FakeContract:
        id = 2
        client = FakeClient()

    class FakeSupport:
        id = 4
        first_name = 'john'
        last_name = 'doe'

    class FakeEvent:
        def __init__(self):
            self.id = 1
            self.contract = FakeContract()
            self.support_contact_id = 4
            self.support_contact = FakeSupport()

    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_assigned_events(self):
            return [FakeEvent(),]

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list', '--assigned'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert '3' in result.output
    assert 'Un Known' in result.output
    assert '2' in result.output
    assert '4' in result.output
    assert 'John Doe' in result.output


def test_get_events_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_all_events(self):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list'])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_get_events_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_events_to_assign(self):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list', '--to-assign'])

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


def test_get_events_displays_error_if_user_does_not_have_support_role(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_assigned_events(self):
            return 'user_not_support_role'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['list', '--assigned'])

    assert result.exit_code == 0
    assert 'Action restricted to the support team.' in result.output


# Test the command detail

def test_get_event_displays_details_of_an_event(monkeypatch):
    class FakeClient:
        id = 3
        first_name = 'Un'
        last_name = 'Known'
        phone_number = '222'
        email = 'client@test.com'

    class FakeContract:
        id = 2
        client_id = 3
        client = FakeClient()

    class FakeSupport:
        id = 4
        first_name = 'john'
        last_name = 'doe'

    class FakeEvent:
        def __init__(self):
            self.id = 1
            self.contract_id = 2
            self.contract = FakeContract()
            self.support_contact_id = 4
            self.support_contact = FakeSupport()
            self.start_date = None
            self.end_date = None
            self.location = None
            self.number_of_attendees = None
            self.notes = None

    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def get_event(self, event_id):
            return FakeEvent()

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(events, ['detail', '--id', '1'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert '3' in result.output
    assert 'Un Known' in result.output
    assert '222' in result.output
    assert 'client@test.com' in result.output
    assert '-' in result.output
    assert '2' in result.output
    assert '4' in result.output
    assert 'John Doe' in result.output


# Test the command update

def test_update_event_displays_success(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def update_event(self, event_id, start_date, end_date,
                         location, number_of_attendees, notes):
            assert event_id == 1
            assert start_date == '02/02/2026'
            assert end_date is None
            assert location == 'berlin'
            assert number_of_attendees is None
            assert notes is None
            return True

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'update',
            '--id', '1',
            '--start-date', '02/02/2026',
            '--location', 'berlin',
        ]
    )

    assert result.exit_code == 0
    assert 'Event successfully updated.' in result.output


def test_update_event_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def update_event(self, event_id, start_date, end_date,
                         location, number_of_attendees, notes):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'update',
            '--id', '1',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_update_event_displays_error_if_event_not_found(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def update_event(self, event_id, start_date, end_date,
                         location, number_of_attendees, notes):
            return 'event_not_found'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'update',
            '--id', '1',
        ]
    )

    assert result.exit_code == 0
    assert 'The event was not found.' in result.output


def test_update_event_displays_error_if_user_not_client_support_contact(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def update_event(self, event_id, start_date, end_date,
                         location, number_of_attendees, notes):
            return 'user_not_client_support_contact'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'update',
            '--id', '1',
        ]
    )

    assert result.exit_code == 0
    assert 'You are not the support contact on this event.' in result.output


# Test the command assign

def test_assign_event_displays_success(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def assign_support_contact(self, event_id, support_contact_id):
            assert support_contact_id == 2
            return True

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'assign',
            '--id', '1',
            '--support-id', '2',
        ]
    )

    assert result.exit_code == 0
    assert 'Support contact successfully updated.' in result.output


def test_assign_event_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def assign_support_contact(self, event_id, support_contact_id):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'assign',
            '--id', '1',
            '--support-id', '2',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_assign_event_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def assign_support_contact(self, event_id, support_contact_id):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'assign',
            '--id', '1',
            '--support-id', '2',
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


def test_assign_event_displays_error_if_support_contact_not_found(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def assign_support_contact(self, event_id, support_contact_id):
            return 'support_contact_not_found'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'assign',
            '--id', '1',
            '--support-id', '2',
        ]
    )

    assert result.exit_code == 0
    assert 'Support contact was not found in users.' in result.output


def test_assign_event_displays_error_if_support_contact_not_support_role(monkeypatch):
    class FakeEventController:
        def __init__(self, event_repository, contract_repository, user_repository):
            pass

        def assign_support_contact(self, event_id, support_contact_id):
            return 'support_contact_not_support_role'

    monkeypatch.setattr('crm.cli.event_cli.EventController', FakeEventController)

    runner = CliRunner()

    result = runner.invoke(
        events,
        [
            'assign',
            '--id', '1',
            '--support-id', '2',
        ]
    )

    assert result.exit_code == 0
    assert 'User enterred for support contact does not have role "support".' in result.output
