import re


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
