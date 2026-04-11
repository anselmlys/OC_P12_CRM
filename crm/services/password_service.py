import base64
import hashlib
import hmac
import os


ITERATIONS = 100_000
SALT_SIZE = 16
HASH_NAME = 'sha256'


def hash_password(password_entered):
    '''Return a salted PBKDF2 hash of the given password as a formatted string.'''
    # Generate 16 randon bytes for salt
    salt = os.urandom(SALT_SIZE)

    # Calculate the hash PBKDF2
    derived_key = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password_entered.encode('utf-8'),
        salt,
        ITERATIONS
    )

    # Transform bytes in python string
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    hash_b64 = base64.b64encode(derived_key).decode('utf-8')

    hashed_password = f'{ITERATIONS}${salt_b64}${hash_b64}'

    return hashed_password


def verify_password(password_entered, stored_password):
    '''Return True if the password matches the stored PBKDF2 hash, else False.'''
    iterations_str, salt_b64, hash_b64 = stored_password.split('$')

    # Convert back to bytes
    iterations = int(iterations_str)
    salt = base64.b64decode(salt_b64.encode('utf-8'))
    stored_hash = base64.b64decode(hash_b64.encode('utf-8'))

    # Recalculate the hash
    derived_key = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password_entered.encode('utf-8'),
        salt,
        iterations
    )

    return hmac.compare_digest(derived_key, stored_hash)
