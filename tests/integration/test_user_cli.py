from click.testing import CliRunner

from crm.cli.user_cli import users


# Test the command create-user

def test_create_user_displays_success(monkeypatch):
    class FakeUser:
        id = 1

    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def create_user(self, email, last_name, first_name, role, password):
            return FakeUser()

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'create',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--first-name', 'Jane',
            '--role', 'sales',
            '--password', 'password123'
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
            'create',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--first-name', 'Jane',
            '--role', 'sales',
            '--password', 'password123'
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
            'create',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--first-name', 'Jane',
            '--role', 'sales',
            '--password', 'password123'
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
            'create',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--first-name', 'Jane',
            '--role', 'sales',
            '--password', 'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'email invalid' in result.output


# Test the command list

def test_get_users_displays_success(monkeypatch):
    class FakeUser:
        def __init__(self, user_id, email, last_name, first_name, role):
            self.id = user_id
            self.email = email
            self.last_name = last_name
            self.first_name = first_name
            self.role = role

    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def get_all_users(self):
            return [
                FakeUser(1, 'jane@test.com', 'doe', 'jane', 'management'),
                FakeUser(2, 'john@test.com', 'doe', 'john', 'sales')
            ]

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, ['list'])

    assert result.exit_code == 0
    assert 'Users' in result.output
    assert 'jane@test.com' in result.output
    assert 'Doe' in result.output
    assert 'Jane' in result.output
    assert 'management' in result.output
    assert 'john@test.com' in result.output
    assert 'sales' in result.output


def test_get_users_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def get_all_users(self):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, ['list'])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_get_users_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def get_all_users(self):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, ['list'])

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


# Test the command update

def test_update_user_displays_success(monkeypatch):
    class FakeUser:
        id = 1

    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def update_user_by_id(self, user_id, email, last_name, first_name, role):
            assert user_id == 1
            assert email == 'test@test.com'
            assert last_name == 'Doe'
            assert first_name is None
            assert role == 'sales'
            return FakeUser()

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'update',
            '--id', '1',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--role', 'sales'
        ]
    )

    assert result.exit_code == 0
    assert 'User successfully updated.' in result.output


def test_update_user_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def update_user_by_id(self, user_id, email, last_name, first_name, role):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'update',
            '--id', '1',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--role', 'sales'
        ]
    )

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_update_user_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def update_user_by_id(self, user_id, email, last_name, first_name, role):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'update',
            '--id', '1',
            '--email', 'test@test.com',
            '--last-name', 'Doe',
            '--role', 'sales'
        ]
    )

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output


def test_update_user_displays_error_if_value_error_raised(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def update_user_by_id(self, user_id, email, last_name, first_name, role):
            raise ValueError('Invalid email.')

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(
        users,
        [
            'update',
            '--id', '1',
            '--email', '@test.com',
            '--last-name', 'Doe',
            '--role', 'sales'
        ]
    )

    assert result.exit_code == 0
    assert 'Error: Invalid email.' in result.output


# Test the command delete

def test_delete_user_displays_success(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def delete_user_by_id(self, user_id):
            return True

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, [
        'delete',
        '--id', '1'
    ])

    assert result.exit_code == 0
    assert 'User successfully deleted.' in result.output


def test_delete_user_displays_error_if_user_not_authenticated(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def delete_user_by_id(self, user_id):
            return 'user_not_authenticated'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, [
        'delete',
        '--id', '1'
    ])

    assert result.exit_code == 0
    assert 'Please login first.' in result.output


def test_delete_user_displays_error_if_user_does_not_have_management_role(monkeypatch):
    class FakeUserController:
        def __init__(self, user_repository):
            pass

        def delete_user_by_id(self, user_id):
            return 'user_not_management_role'

    monkeypatch.setattr('crm.cli.user_cli.UserController', FakeUserController)

    runner = CliRunner()

    result = runner.invoke(users, [
        'delete',
        '--id', '1'
    ])

    assert result.exit_code == 0
    assert 'Action restricted to the management team.' in result.output
