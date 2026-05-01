from click.testing import CliRunner

from crm.models.user import User
from crm.cli.db_cli import db


# Test the command create-admin

def test_create_admin_create_user_and_displays_success(session, user_repo, monkeypatch):
    monkeypatch.setattr('crm.cli.db_cli.Session', lambda: session)

    runner = CliRunner()

    result = runner.invoke(
        db,
        [
            'create-admin',
            '--email', '  test@test.com',
            '--last-name', 'min ',
            '--first-name', 'ad',
            '--password', 'password123'
        ]
    )

    assert result.exit_code == 0
    assert 'First management user created successfully.' in result.output

    new_user = session.query(User).filter(User.id == 1).first()

    assert new_user is not None
    assert new_user.email == 'test@test.com'
    assert new_user.last_name == 'min'
    assert new_user.first_name == 'ad'
    assert new_user.role == 'management'
