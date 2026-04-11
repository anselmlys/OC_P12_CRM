import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
EXPIRATION_MINUTES = 60
TOKEN_FILE = Path('.session_token')


def create_access_token(user):
    '''Create JWT token containing user id and role.'''
    if not SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY is missing from .env file.')
    
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user.id),
        'role': user.role,
        'iat': now,
        'exp': now + timedelta(minutes=EXPIRATION_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def save_token(token):
    '''Save the JWT token to a local file.'''
    try:
        TOKEN_FILE.write_text(token, encoding='utf-8')
    except OSError as e:
        raise RuntimeError(f'Failed to save token: {e}') from e


def load_token():
    '''Load the JWT token from the local file, return None if not found.'''
    try:
        if not TOKEN_FILE.exists():
            return None
        token = TOKEN_FILE.read_text(encoding='utf-8').strip()
        return token
    except OSError as e:
        raise RuntimeError(f'Failed to load token: {e}') from e


def delete_token():
    '''Delete the stored JWT token file if it exists.'''
    try:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
    except OSError as e:
        raise RuntimeError(f'Failed to delete token: {e}') from e


def decode_access_token(token):
    '''Decode and validate a JWT token, returning its payload.'''
    if not SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY is missing from .env file.')
    
    token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return token_payload
