from click.testing import CliRunner

from crm.cli.user_cli import users


# Test the command create-user

def test_create_user_displays_success(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def create_user(self, email, last_name, first_name, role, password):
            return True
    
    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'create-user',
            '--email',
            'test@test.com',
            '--last-name',
            'Doe',
            '--first-name',
            'Jane',
            '--role',
            'sales',
            '--password',
            'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'User successfully created.' in result.output


def test_create_user_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def create_user(self, email, last_name, first_name, role, password):
            return 'user_not_authenticated'
    
    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'create-user',
            '--email',
            'test@test.com',
            '--last-name',
            'Doe',
            '--first-name',
            'Jane',
            '--role',
            'sales',
            '--password',
            'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_create_user_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def create_user(self, email, last_name, first_name, role, password):
            return 'user_not_management_role'
    
    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'create-user',
            '--email',
            'test@test.com',
            '--last-name',
            'Doe',
            '--first-name',
            'Jane',
            '--role',
            'sales',
            '--password',
            'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


def test_create_user_displays_error_if_value_or_type_error_raised(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def create_user(self, email, last_name, first_name, role, password):
            raise ValueError('email invalid')
    
    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'create-user',
            '--email',
            'test@test.com',
            '--last-name',
            'Doe',
            '--first-name',
            'Jane',
            '--role',
            'sales',
            '--password',
            'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'email invalid' in result.output
