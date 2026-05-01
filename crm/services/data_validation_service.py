import re
from datetime import datetime


def clean_password(value):
    '''Validate password format and return it if valid.'''
    password_format = r'[A-Za-z0-9!?@#$%^&+*=\-_]{8,}'
    if not re.fullmatch(password_format, value):
        raise ValueError('password must be at least 8 characters'
                         'and can include the symbols !?@#$%^&+*=-_')

    return value


def clean_required_string(value, field_name):
    '''Strip a required string and raise an error if it is empty.'''
    if value is None:
        raise ValueError(f'{field_name} is required')

    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError(f'{field_name} is required')

    return cleaned_value


def clean_optional_string(value):
    '''Strip an optional string and return None if it is empty.'''
    if value is None:
        return None

    cleaned_value = value.strip()

    if not cleaned_value:
        return None

    return cleaned_value


def clean_email(email):
    '''Strip and validate an email address.'''
    cleaned_email = clean_required_string(email, 'email').lower()

    email_pattern = r'[^@\s]+@[^@\s]+\.[^@\s]+'
    if not re.match(email_pattern, cleaned_email):
        raise ValueError('email format is invalid')

    return cleaned_email


def clean_required_integer(value, field_name):
    '''
    Convert a required string into an integer and raise an error if it is empty or invalid.
    '''
    if value is None:
        raise ValueError(f'{field_name} is required')

    if isinstance(value, str):
        value = value.strip()

    if not value:
        raise ValueError(f'{field_name} is required')

    try:
        value = int(value)
        return value

    except (ValueError, TypeError):
        raise ValueError(f'{field_name} must be an integer')


def clean_optional_integer(value, field_name):
    '''
    Convert an optional string into an integer, return none if it is empty
    and raise an error if it is invalid.
    '''
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()

    if value == '':
        return None

    try:
        value = int(value)
        return value

    except (ValueError, TypeError):
        raise ValueError(f'{field_name} must be an integer')


def clean_optional_boolean(value, field_name):
    '''
    Convert a "yes" or "no" string into a boolean, return none if it is empty
    and raise an error if it invalid.
    '''
    if value is None:
        return False

    value = value.strip().lower()

    if value == 'yes':
        return True
    elif value == 'no':
        return False
    else:
        raise ValueError(f'"{value}" is invalid: {field_name} must be yes or no')


def clean_optional_date(value, field_name):
    '''
    Convert a DD/MM/YYYY string into a date and raise an error if it is invalid.
    '''
    if value is None:
        return None

    value = value.strip()
    if not value:
        return None

    try:
        value = datetime.strptime(value, '%d/%m/%Y').date()
        return value
    except ValueError:
        raise ValueError(f'"{value}" is invalid: {field_name} must respect the format DD/MM/YYYY')


def clean_role(value):
    '''Verify role string and raise an error if it invalid.'''
    if value is None:
        raise ValueError('role is required')

    value = value.strip()
    if not value:
        raise ValueError('role is required')

    if value == 'management':
        return 'management'
    elif value == 'support':
        return 'support'
    elif value == 'sales':
        return 'sales'
    else:
        raise ValueError(f'{value} is invalid: role must be management or support or sales')
