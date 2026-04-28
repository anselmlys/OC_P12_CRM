from click.testing import CliRunner
from datetime import datetime, timezone

from crm.cli.client_cli import clients


# Test the command create

def test_create_client_displays_success(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def create_client(self, last_name, first_name,
                          email, phone_number=None, company_name=None):
            return True

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'create',
            '--last-name', 'doe',
            '--first-name', 'jane',
            '--email', 'janedoe@test.com',
            '--company-name', 'Test Company'
        ]
    )

    assert result.exit_code == 0
    assert 'Client successfully created.' in result.output


def test_create_client_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def create_client(self, last_name, first_name,
                          email, phone_number=None, company_name=None):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'create',
            '--last-name', 'doe',
            '--first-name', 'jane',
            '--email', 'janedoe@test.com',
            '--company-name', 'Test Company'
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_create_client_displays_error_if_user_does_not_have_sales_role(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def create_client(self, last_name, first_name,
                          email, phone_number=None, company_name=None):
            return 'user_not_sales_role'

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'create',
            '--last-name', 'doe',
            '--first-name', 'jane',
            '--email', 'janedoe@test.com',
            '--company-name', 'Test Company'
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the sales team.' in result.output


def test_create_client_displays_error_if_value_error_is_raised(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def create_client(self, last_name, first_name,
                          email, phone_number=None, company_name=None):
            raise ValueError('Email invalid.')

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'create',
            '--last-name', 'doe',
            '--first-name', 'jane',
            '--email', '@test.com',
            '--company-name', 'Test Company'
        ]
    )

    assert result.exit_code == 0
    assert 'Email invalid.' in result.output


def test_create_client_displays_error_if_runtime_error_is_raised(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def create_client(self, last_name, first_name,
                          email, phone_number=None, company_name=None):
            raise RuntimeError('Session has crashed.')

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'create',
            '--last-name', 'doe',
            '--first-name', 'jane',
            '--email', '@test.com',
            '--company-name', 'Test Company'
        ]
    )

    assert result.exit_code == 0
    assert 'Session has crashed.' in result.output


# Test the command list

def test_get_clients_displays_success(monkeypatch):
    class FakeSalesContact:
        first_name = 'Jane'
        last_name = 'Doe'


    class FakeClient:
        def __init__(self):
            self.id = 1
            self.last_name = 'doe'
            self.first_name = 'john'
            self.email = 'test@test.com'
            self.company_name = None
            self.sales_contact_id = 2
            self.sales_contact = FakeSalesContact()
            
        
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def get_all_clients(self):
            return [FakeClient()]

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(clients, ['list'])

    assert result.exit_code == 0
    assert 'Clients' in result.output
    assert 'John Doe' in result.output
    assert 'test@test.com' in result.output
    assert '-' in result.output
    assert 'Jane Doe' in result.output


def test_get_clients_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def get_all_clients(self):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(clients, ['list'])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


# Test the command detail

def test_get_client_displays_success(monkeypatch):
    class FakeSalesContact:
        id = 2
        first_name = 'Jane'
        last_name = 'Doe'


    class FakeClient:
        def __init__(self):
            self.id = 1
            self.last_name = 'doe'
            self.first_name = 'john'
            self.email = 'test@test.com'
            self.phone_number = None
            self.company_name = 'test company'
            self.created_at = datetime(2026, 2, 2, 10, 0, tzinfo=timezone.utc)
            self.updated_at = datetime(2026, 2, 4, 15, 30, tzinfo=timezone.utc)
            self.sales_contact_id = 2
            self.sales_contact = FakeSalesContact()
            
    client = FakeClient()
        
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def get_client(self, client_id):
            return client

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(clients, ['detail', '--id', 1])

    assert result.exit_code == 0
    assert 'John Doe' in result.output
    assert 'test@test.com' in result.output
    assert '-' in result.output
    assert 'Test Company' in result.output
    assert '02/02/' in result.output
    assert '04/02/' in result.output
    assert 'Jane Doe' in result.output


def test_get_client_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def get_client(self, client_id):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(clients, ['detail', '--id', 1])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


# Test the command update

def test_update_client_displays_success(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def update_client(self, client_id, last_name, first_name, email, phone_number, company_name):
            assert client_id == 1
            assert last_name == 'doe'
            assert first_name is None
            assert email is None
            assert phone_number is None
            assert company_name == 'test company'
            return True
        
    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'update',
            '--id', '1',
            '--last-name', 'doe',
            '--company-name', 'test company',
        ]
    )

    assert result.exit_code == 0
    assert 'Client successfully updated.' in result.output


def test_update_client_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def update_client(self, client_id, last_name, first_name, email, phone_number, company_name):
            return 'user_not_authenticated'
        
    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'update',
            '--id', '1',
            '--last-name', 'doe',
            '--company-name', 'test company',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_update_client_displays_error_if_user_does_not_have_sales_role(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def update_client(self, client_id, last_name, first_name, email, phone_number, company_name):
            return 'user_not_sales_role'
        
    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'update',
            '--id', '1',
            '--last-name', 'doe',
            '--company-name', 'test company',
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the sales team.' in result.output


def test_update_client_displays_error_if_client_not_found(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def update_client(self, client_id, last_name, first_name, email, phone_number, company_name):
            return 'client_not_found'
        
    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'update',
            '--id', '1',
            '--last-name', 'doe',
            '--company-name', 'test company',
        ]
    )

    assert result.exit_code == 0
    assert 'Client was not found.' in result.output


def test_update_client_displays_error_if_user_not_client_contact(monkeypatch):
    class FakeClientController:
        def __init__(self, client_repository):
            pass

        def update_client(self, client_id, last_name, first_name, email, phone_number, company_name):
            return 'user_not_client_contact'
        
    monkeypatch.setattr('crm.cli.client_cli.ClientController', FakeClientController)

    runner = CliRunner()

    result = runner.invoke(
        clients,
        [
            'update',
            '--id', '1',
            '--last-name', 'doe',
            '--company-name', 'test company',
        ]
    )

    assert result.exit_code == 0
    assert 'You are not the contact of this client.' in result.output
