from click.testing import CliRunner

from crm.cli.auth_cli import auth


# Test the command login

def test_login_command_displays_success(monkeypatch):
    class FakeAuthController:
        def __init__(self, session, user_repository):
            pass

        def login(self, email, password):
            return True
        
    monkeypatch.setattr('crm.cli.auth_cli.AuthController', FakeAuthController)

    runner = CliRunner()

    result = runner.invoke(
        auth,
        ['login', '--email', 'test@test.com', '--password', 'password123'],
    )

    assert result.exit_code == 0
    assert 'Login successful!' in result.output


def test_login_command_displays_error_if_user_not_found(monkeypatch):
    class FakeAuthController:
        def __init__(self, session, user_repository):
            pass

        def login(self, email, password):
            return 'user_not_found'
        
    monkeypatch.setattr('crm.cli.auth_cli.AuthController', FakeAuthController)

    runner = CliRunner()

    result = runner.invoke(
        auth,
        ['login', '--email', 'test@test.com', '--password', 'password123'],
    )

    assert result.exit_code == 0
    assert 'User not found.' in result.output


def test_login_command_displays_error_if_password_invalid(monkeypatch):
    class FakeAuthController:
        def __init__(self, session, user_repository):
            pass

        def login(self, email, password):
            return 'invalid_password'
        
    monkeypatch.setattr('crm.cli.auth_cli.AuthController', FakeAuthController)

    runner = CliRunner()

    result = runner.invoke(
        auth,
        ['login', '--email', 'test@test.com', '--password', 'password123'],
    )

    assert result.exit_code == 0
    assert 'Password invalid.' in result.output
