import jwt
import pytest

from crm.services import token_service


class DummyUser:
    def __init__(self, id, role):
        self.id = id
        self.role = role


@pytest.fixture
def set_test_secret_key(monkeypatch):
    monkeypatch.setattr(token_service, 'SECRET_KEY', 'test-secret-key')


@pytest.fixture
def token_file(tmp_path, monkeypatch):
    test_file = tmp_path / '.session_token'
    monkeypatch.setattr(token_service, 'TOKEN_FILE', test_file)
    return test_file


# Test the function create_access_token

def test_create_access_token_returns_token(set_test_secret_key):
    user = DummyUser(id=1, role='sales')
    token = token_service.create_access_token(user)

    decoded_payload = jwt.decode(
        token,
        'test-secret-key',
        algorithms=[token_service.ALGORITHM]
    )

    assert decoded_payload['sub'] == '1'
    assert decoded_payload['role'] == 'sales'
    assert 'iat' in decoded_payload
    assert 'exp' in decoded_payload


def test_create_access_token_raises_error_if_secret_key_missing(monkeypatch):
    monkeypatch.setattr(token_service, 'SECRET_KEY', None)

    user = DummyUser(1, 'sales')

    with pytest.raises(
        ValueError,
        match='JWT_SECRET_KEY is missing from .env file.'
    ):
        token_service.create_access_token(user)


# Test the function save_token

def test_save_token_writes_token_to_file(token_file):
    token_service.save_token('my-test-token')

    assert token_file.exists()
    assert token_file.read_text(encoding='utf-8') == 'my-test-token'


# Test the function load_token

def test_load_token_returns_none_if_file_does_not_exist(token_file):
    loaded_token = token_service.load_token()

    assert loaded_token is None


def test_load_token_returns_file_content(token_file):
    token_file.write_text('stored-token', encoding='utf-8')

    loaded_token = token_service.load_token()

    assert loaded_token == 'stored-token'


# Test the function delete_token

def test_delete_token_removes_file(token_file):
    token_file.write_text("stored-token", encoding="utf-8")

    token_service.delete_token()

    assert not token_file.exists()


def test_delete_token_does_nothing_if_file_does_not_exist(token_file):
    token_service.delete_token()

    assert not token_file.exists()


# Test the function decode_access_token

def test_decode_access_token_returns_payload(set_test_secret_key):
    user = DummyUser(id=1, role='sales')
    token = token_service.create_access_token(user)

    payload = token_service.decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "sales"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_access_token_raises_error_if_secret_key_is_missing(monkeypatch):
    monkeypatch.setattr(token_service, "SECRET_KEY", None)

    with pytest.raises(ValueError, match="JWT_SECRET_KEY is missing from .env file."):
        token_service.decode_access_token("fake-token")


def test_decode_access_token_raises_error_for_invalid_token(set_test_secret_key):
    with pytest.raises(jwt.InvalidTokenError):
        token_service.decode_access_token("not-a-real-token")
