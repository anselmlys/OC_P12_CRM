from jwt import ExpiredSignatureError, InvalidTokenError

from crm.repositories.user_repository import UserRepository
from crm.services.password_service import hash_password, verify_password
from crm.services.token_service import (create_access_token, save_token,
                                        delete_token, load_token, decode_access_token)


def create_user(user_repository, email, last_name, first_name, password_entered, role):
    '''Create a new user with a hashed password and store it in the db.'''
    hashed_password = hash_password(password_entered)

    user = user_repository.create_user(email, last_name, first_name, hashed_password, role)
    
    return user


def login(session, email, password_entered):
    '''Authenticate a user and store a JWT token if credentials are valid.'''
    repo = UserRepository(session)
    user = repo.get_by_email(email)
    if user is None:
        return 'user_not_found'
    
    is_valid = verify_password(
        password_entered,
        user.hashed_password,
    )

    if not is_valid:
        return 'invalid_password'
    
    token = create_access_token(user)
    save_token(token)
    
    return True


def logout():
    '''Delete the stored JWT token to log out the user.'''
    delete_token()


def get_current_user_payload():
    '''Return the decoded JWT payload if valid, else None.'''
    token = load_token()

    if token is None:
        return None
    
    try:
        return decode_access_token(token)
    except ExpiredSignatureError:
        delete_token()
        return None
    except InvalidTokenError:
        delete_token()
        return None
