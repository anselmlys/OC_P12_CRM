from click.testing import CliRunner
from datetime import datetime, timezone

from crm.cli.contract_cli import contracts


# Test the command create

def test_create_contract_displays_success(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def create_contract(self, client_id, total_amount, remaining_amount, signed):
            return True

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'create',
            '--client-id', '1',
            '--total-amount', '500',
            '--remaining-amount', '500',
        ]
    )

    assert result.exit_code == 0
    assert 'Contract successfully created.' in result.output


def test_create_contract_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def create_contract(self, client_id, total_amount, remaining_amount, signed):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'create',
            '--client-id', '1',
            '--total-amount', '500',
            '--remaining-amount', '500',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_create_contract_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def create_contract(self, client_id, total_amount, remaining_amount, signed):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'create',
            '--client-id', '1',
            '--total-amount', '500',
            '--remaining-amount', '500',
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


def test_create_contract_displays_error_if_value_error_raised(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def create_contract(self, client_id, total_amount, remaining_amount, signed):
            raise ValueError('Invalid value.')

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'create',
            '--client-id', '1',
            '--total-amount', '500',
            '--remaining-amount', '500',
        ]
    )

    assert result.exit_code == 0
    assert 'Error: Invalid value.' in result.output


def test_create_contract_displays_error_if_runtime_error_raised(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def create_contract(self, client_id, total_amount, remaining_amount, signed):
            raise RuntimeError('Session has crashed.')

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'create',
            '--client-id', '1',
            '--total-amount', '500',
            '--remaining-amount', '500',
        ]
    )

    assert result.exit_code == 0
    assert 'Error: Session has crashed.' in result.output


# Test the command list

def test_get_contracts_displays_list_of_contracts(monkeypatch):
    class FakeClient:
        id = 2
        first_name = 'Un'
        last_name = 'Known'

    class FakeEvent:
        id = 3

    class FakeContract:
        def __init__(self):
            self.id = 1
            self.client = FakeClient()
            self.event = FakeEvent()

    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_all_contracts(self):
            return [FakeContract(),]

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['list'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert 'Contracts' in result.output
    assert 'Un Known' in result.output
    assert '3' in result.output


def test_get_contracts_displays_list_of_unsigned_contracts(monkeypatch):
    class FakeClient:
        id = 2
        first_name = 'Un'
        last_name = 'Known'

    class FakeEvent:
        id = 3

    class FakeContract:
        def __init__(self):
            self.id = 1
            self.client = FakeClient()
            self.event = FakeEvent()
            self.signed = True

    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_unsigned_contracts(self):
            return [FakeContract(),]

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['list', '--unsigned'])

    assert result.exit_code == 0
    assert '1' in result.output
    assert 'Contracts' in result.output
    assert 'Un Known' in result.output
    assert '3' in result.output


def test_get_contracts_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_all_contracts(self):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['list'])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_get_contracts_displays_error_if_user_does_not_have_sales_role(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_all_contracts(self):
            return 'user_not_sales_role'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['list'])

    assert result.exit_code == 0
    assert 'Action restricted to the sales team.' in result.output


# Test the command detail

def test_get_contract_displays_contract_detail(monkeypatch):
    class FakeClient:
        id = 2
        first_name = 'Un'
        last_name = 'Known'

    class FakeEvent:
        id = 3

    class FakeContract:
        def __init__(self):
            self.id = 1
            self.client = FakeClient()
            self.event = FakeEvent()
            self.total_amount = 500
            self.remaining_amount = None
            self.created_at = datetime(2026, 2, 2, 10, 0, tzinfo=timezone.utc)
            self.signed = True

    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_contract(self, contract_id):
            return FakeContract()

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['detail', '--id', '1'])

    assert result.exit_code == 0
    assert 'Contract #1' in result.output
    assert '2' in result.output
    assert 'Un Known' in result.output
    assert '500' in result.output
    assert '-' in result.output
    assert '02/02/' in result.output
    assert 'Yes' in result.output
    assert '3' in result.output


def test_get_contract_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def get_contract(self, contract_id):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(contracts, ['detail', '--id', '1'])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


# Test the command update

def test_update_contract_displays_success(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def update_contract(self, contract_id, client_id, total_amount, remaining_amount, signed):
            assert client_id == 2
            assert total_amount == 500
            assert remaining_amount is None
            assert signed == 'yes'
            return True

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'update',
            '--id', '1',
            '--client-id', '2',
            '--total-amount', '500',
            '--signed', 'yes',
        ]
    )

    assert result.exit_code == 0
    assert 'Contract successfully updated.' in result.output


def test_update_contract_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def update_contract(self, contract_id, client_id, total_amount, remaining_amount, signed):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'update',
            '--id', '1',
            '--client-id', '2',
            '--total-amount', '500',
            '--signed', 'yes',
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_update_contract_displays_error_if_contract_not_found(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def update_contract(self, contract_id, client_id, total_amount, remaining_amount, signed):
            return 'contract_not_found'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'update',
            '--id', '1',
            '--client-id', '2',
            '--total-amount', '500',
            '--signed', 'yes',
        ]
    )

    assert result.exit_code == 0
    assert 'Contract not found.' in result.output


def test_update_contract_displays_error_if_user_not_client_contact(monkeypatch):
    class FakeContractController:
        def __init__(self, contract_repository):
            pass

        def update_contract(self, contract_id, client_id, total_amount, remaining_amount, signed):
            return 'user_not_client_contact'

    monkeypatch.setattr('crm.cli.contract_cli.ContractController', FakeContractController)

    runner = CliRunner()

    result = runner.invoke(
        contracts,
        [
            'update',
            '--id', '1',
            '--client-id', '2',
            '--total-amount', '500',
            '--signed', 'yes',
        ]
    )

    assert result.exit_code == 0
    assert 'You are not the contact of this client.' in result.output
