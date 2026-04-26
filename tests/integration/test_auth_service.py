import pytest
from jwt import ExpiredSignatureError, InvalidTokenError

from crm.services import auth_service


class DummyUser:
    def __init__(self, email, hashed_password):
        self.email = email
        self.hashed_password = hashed_password


# Test the function login

def test_login_returns_false_if_user_not_found(monkeypatch):
    class DummyRepo:
        def get_by_email(self, email):
            return None
    
    monkeypatch.setattr(auth_service, 'UserRepository', lambda session: DummyRepo())

    result = auth_service.login(None, 'test@test.com', 'password')

    assert result == 'user_not_found'


def test_login_returns_false_if_password_is_invalid(monkeypatch):
    dummy_user = DummyUser('test@test.com', 'hashed_password')

    class DummyRepo:
        def get_by_email(self, email):
            return dummy_user
    
    monkeypatch.setattr(auth_service, 'UserRepository', lambda session: DummyRepo())
    monkeypatch.setattr(auth_service, 'verify_password', lambda p, h: False)

    result = auth_service.login(None, 'test@test.com', 'wrong-password')

    assert result == 'invalid_password'


# Test the function get_current_user_payload

def test_get_current_user_payload_returns_none_if_no_token_found(monkeypatch):
    monkeypatch.setattr(auth_service, 'load_token', lambda: None)

    result = auth_service.get_current_user_payload()

    assert result is None


def test_get_current_user_payload_returns_payload_if_token_is_valid(monkeypatch):
    monkeypatch.setattr(auth_service, 'load_token', lambda: 'fake-token')
    fake_payload = {'sub': 1, 'role': 'sales'}

    monkeypatch.setattr(
        auth_service,
        'decode_access_token',
        lambda token: fake_payload,
    )

    result = auth_service.get_current_user_payload()

    assert result == fake_payload


def test_get_current_user_payload_deletes_token_and_returns_none_if_token_is_expired(monkeypatch):
    monkeypatch.setattr(auth_service, "load_token", lambda: "fake-token")

    def fake_decode_access_token(token):
        raise ExpiredSignatureError

    monkeypatch.setattr(auth_service, "decode_access_token", fake_decode_access_token)

    delete_called = {"value": False}
    def fake_delete_token():
        delete_called["value"] = True
    
    monkeypatch.setattr(auth_service, "delete_token", fake_delete_token)

    result = auth_service.get_current_user_payload()

    assert result is None
    assert delete_called['value'] is True


def test_get_current_user_payload_deletes_token_and_returns_none_if_token_is_invalid(monkeypatch):
    monkeypatch.setattr(auth_service, "load_token", lambda: "fake-token")

    def fake_decode_access_token(token):
        raise InvalidTokenError

    monkeypatch.setattr(auth_service, "decode_access_token", fake_decode_access_token)

    delete_called = {"value": False}
    def fake_delete_token():
        delete_called["value"] = True
    
    monkeypatch.setattr(auth_service, "delete_token", fake_delete_token)

    result = auth_service.get_current_user_payload()

    assert result is None
    assert delete_called['value'] is True
