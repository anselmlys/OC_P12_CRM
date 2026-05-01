import base64

from crm.services import password_service


# Test the function hash_password

def test_hash_password_returns_valid_formatted_hash():
    password_entered = 'test-password'

    hashed_password = password_service.hash_password(password_entered)

    parts = hashed_password.split('$')
    assert len(parts) == 3

    iterations_str, salt_b64, hash_b64 = parts

    assert iterations_str == str(password_service.ITERATIONS)

    salt = base64.b64decode(salt_b64.encode('utf-8'))
    assert len(salt) == password_service.SALT_SIZE

    derived_key = base64.b64decode(hash_b64.encode('utf-8'))
    assert len(derived_key) > 0


def test_hash_password_returns_different_hashes_for_same_password():
    password = 'test-password'

    hash_1 = password_service.hash_password(password)
    hash_2 = password_service.hash_password(password)

    assert hash_1 != hash_2


# Test the function verify_password

def test_verify_password_returns_true_if_entered_and_stored_password_match():
    password = 'test-password'

    stored_password = password_service.hash_password(password)

    assert password_service.verify_password(password, stored_password)


def test_verify_password_returns_false_if_passwords_do_not_match():
    password_1 = 'test-password'
    stored_password = password_service.hash_password(password_1)

    password_2 = 'other-test-password'

    assert not password_service.verify_password(password_2, stored_password)
