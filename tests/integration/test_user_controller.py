from crm.models.user import User
from crm.services.password_service import verify_password


# Test the method create_user

def test_create_user_returns_new_user(
        user_controller,
        monkeypatch,
        management_payload,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: management_payload)
    
    password_entered='motdepasse123'

    result = user_controller.create_user(
        email='  user-test@test.com ',
        last_name='Un  ',
        first_name='Known',
        password_entered=password_entered,
        role='support'
    )

    assert result is not None
    assert result.id is not None
    assert result.email == 'user-test@test.com'
    assert result.last_name == 'Un'
    assert result.first_name == 'Known'
    assert result.role == 'support'
    assert verify_password(password_entered, result.hashed_password)

    new_user = session.query(User).filter(User.id == result.id).first()

    assert new_user is not None
    assert new_user.email == result.email
    assert verify_password(password_entered, new_user.hashed_password)


def test_create_user_returns_none_if_user_not_authenticated(
        monkeypatch,
        user_controller,
        session
    ):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: None)
    
    result = user_controller.create_user(
        email='  user-test@test.com ',
        last_name='Un  ',
        first_name='Known',
        password_entered='mdp123',
        role='support'
    )

    assert result == 'user_not_authenticated'
    assert session.query(User).count() == 0


def test_create_user_returns_none_if_user_does_not_have_management_role(
        monkeypatch,
        user_controller,
        session,
        sales_payload
    ):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    result = user_controller.create_user(
        email='  user-test@test.com ',
        last_name='Un  ',
        first_name='Known',
        password_entered='mdp123',
        role='support'
    )

    assert result == 'user_not_management_role'
    assert session.query(User).count() == 0


# Test the method update_user_by_id

def test_update_user_by_id_returns_updated_user_data(
        monkeypatch,
        management_payload,
        user,
        user_controller,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = user_controller.update_user_by_id(
        user_id=user.id,
        email='  update-test@test.com ',
        last_name=' Up   ',
        first_name=' date  ',
        role=' management'
    )

    assert result is not None
    assert result.email == 'update-test@test.com'
    assert result.last_name == 'Up'
    assert result.first_name == 'date'
    assert result.role == 'management'

    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user is not None
    assert updated_user.email == result.email
    assert updated_user.last_name == result.last_name
    assert updated_user.first_name == result.first_name
    assert updated_user.role == result.role


def test_update_user_by_id_returns_none_if_user_not_authenticated(
        monkeypatch,
        user,
        user_controller,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: None)
    
    result = user_controller.update_user_by_id(
        user_id=user.id,
        email='  update-test@test.com ',
        last_name=' Up   ',
        first_name=' date  ',
        role=' management'
    )

    assert result == 'user_not_authenticated'

    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user is not None
    assert updated_user.email == 'employee-test@test.com'


def test_update_user_by_id_returns_none_if_user_does_not_have_management_role(
        monkeypatch,
        sales_payload,
        user,
        user_controller,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    result = user_controller.update_user_by_id(
        user_id=user.id,
        email='  update-test@test.com ',
        last_name=' Up   ',
        first_name=' date  ',
        role=' management'
    )

    assert result == 'user_not_management_role'

    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user is not None
    assert updated_user.email == 'employee-test@test.com'


# Test the method delete_user_by_id

def test_delete_user_by_id_returns_true_if_deletion_completed(
        monkeypatch,
        management_payload,
        user_controller,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: management_payload)
    
    result = user_controller.delete_user_by_id(user.id)

    assert result is True
    assert session.query(User).count() == 0


def test_delete_user_by_id_returns_false_if_user_not_authenticated(
        monkeypatch,
        user_controller,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: None)
    
    result = user_controller.delete_user_by_id(user.id)

    assert result is False

    user = session.query(User).filter(User.id == user.id).first()

    assert user is not None


def test_delete_user_by_id_returns_false_if_user_does_not_have_management_role(
        monkeypatch,
        sales_payload,
        user_controller,
        user,
        session
):
    monkeypatch.setattr('crm.controllers.user_controller.get_current_user_payload',
                        lambda: sales_payload)
    
    result = user_controller.delete_user_by_id(user.id)

    assert result is False

    user = session.query(User).filter(User.id == user.id).first()

    assert user is not None
