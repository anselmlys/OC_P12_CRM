from crm.models.user import User


# Test the method change_password

def test_change_password_returns_true(
        auth_controller,
        session,
        monkeypatch,
        user,
        sales_payload
    ):
    monkeypatch.setattr('crm.services.auth_service.get_current_user_payload',
                        lambda: sales_payload)
    
    monkeypatch.setattr('crm.controllers.auth_controller.verify_password',
                        lambda password, stored_password: True)
    
    monkeypatch.setattr('crm.controllers.auth_controller.hash_password',
                        lambda password: 'new-hashed-password')

    result = auth_controller.change_password('old-password', 'test-password')

    assert result is True

    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user.hashed_password == 'new-hashed-password'


def test_change_password_returns_false_if_user_not_authenticated(
        auth_controller,
        monkeypatch,
    ):
    monkeypatch.setattr('crm.services.auth_service.get_current_user_payload',
                        lambda: None)

    result = auth_controller.change_password('old-password', 'test-password')

    assert result is False


def test_change_password_returns_false_if_user_not_found(
        auth_controller,
        monkeypatch,
        sales_payload
    ):
    monkeypatch.setattr('crm.services.auth_service.get_current_user_payload',
                        lambda: sales_payload)

    result = auth_controller.change_password('old-password', 'test-password')

    assert result is False


def test_change_password_returns_false_if_password_invalid(
        auth_controller,
        monkeypatch,
        sales_payload,
        user
    ):
    monkeypatch.setattr('crm.services.auth_service.get_current_user_payload',
                        lambda: sales_payload)

    monkeypatch.setattr('crm.controllers.auth_controller.verify_password',
                        lambda password, stored_password: False)

    result = auth_controller.change_password('invalid', 'test-password')

    assert result is False
