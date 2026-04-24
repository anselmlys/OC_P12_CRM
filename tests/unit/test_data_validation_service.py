import pytest
from datetime import date

from crm.services import data_validation_service


# Test the function clean_password

def test_clean_password_returns_valid_password():
    password = 'AbC09!?@#$%^&+*=-_'

    result = data_validation_service.clean_password(password)

    assert result == password


def test_clean_password_raises_error_if_less_than_8_characters():
    password = 'abcdefr'

    with pytest.raises(ValueError):
        data_validation_service.clean_password(password)


def test_clean_password_raises_error_if_contains_spaces():
    password = 'mot de passe'

    with pytest.raises(ValueError):
        data_validation_service.clean_password(password)


def test_clean_password_raises_error_if_empty_string():
    password = ''

    with pytest.raises(ValueError):
        data_validation_service.clean_password(password)


# Test the function clean_required_string

def test_clean_required_string_returns_cleaned_string():
    value = ' doe '
    field_name = 'last_name'

    cleaned_value = data_validation_service.clean_required_string(value, field_name)

    assert cleaned_value == 'doe'

def test_clean_required_string_raises_error_if_string_is_empty():
    value = ' '
    field_name = 'last_name'

    with pytest.raises(ValueError):
        data_validation_service.clean_required_string(value, field_name)

def test_clean_required_string_raises_error_if_field_is_none():
    value = None
    field_name = 'last_name'

    with pytest.raises(ValueError):
        data_validation_service.clean_required_string(value, field_name)


# Test the function clean_optional_string

def test_clean_optional_string_returns_cleaned_string():
    value = ' Fake company name 1'

    cleaned_value = data_validation_service.clean_optional_string(value)

    assert cleaned_value == 'Fake company name 1'

def test_clean_optional_string_returns_none_if_field_is_empty():
    value = '   '

    cleaned_value = data_validation_service.clean_optional_string(value)

    assert cleaned_value is None

def test_clean_optional_string_returns_none_if_field_is_none():
    value = None

    cleaned_value = data_validation_service.clean_optional_string(value)

    assert cleaned_value is None


# Test the function clean_email

def test_clean_email_returns_cleaned_email():
    email = ' Test@tEst.com '

    cleaned_email = data_validation_service.clean_email(email)

    assert cleaned_email == 'test@test.com'

def test_clean_email_raises_error_if_email_format_is_invalid():
    email = ' @test.'

    with pytest.raises(ValueError):
        data_validation_service.clean_email(email)


# Test the function clean_required_integer

def test_clean_required_integer_returns_cleaned_integer():
    value = ' 5    '

    result = data_validation_service.clean_required_integer(value, 'total_amount')

    assert result == 5

def test_clean_required_integer_raises_error_if_field_is_none():
    value = None

    with pytest.raises(ValueError):
        data_validation_service.clean_required_integer(value, 'total_amount')

def test_clean_required_integer_raises_error_if_field_is_empty():
    value = '  '

    with pytest.raises(ValueError):
        data_validation_service.clean_required_integer(value, 'total_amount')

def test_clean_required_integer_raises_error_if_field_is_not_integer():
    value = ' abc '

    with pytest.raises(ValueError):
        data_validation_service.clean_required_integer(value, 'total_amount')


# Test the function clean_optional_integer

def test_clean_optional_integer_returns_cleaned_integer():
    value = ' 5    '

    result = data_validation_service.clean_optional_integer(value, 'total_amount')

    assert result == 5

def test_clean_optional_integer_returns_none_if_field_is_none():
    value = None

    result = data_validation_service.clean_optional_integer(value, 'total_amount')

    assert result == None

def test_clean_optional_integer_returns_none_if_field_is_empty():
    value = '  '

    result = data_validation_service.clean_optional_integer(value, 'total_amount')

    assert result == None

def test_clean_optional_integer_raises_error_if_field_is_not_integer():
    value = '  abc '

    with pytest.raises(ValueError):
        data_validation_service.clean_optional_integer(value, 'total_amount')


# Test the function clean_boolean

def test_clean_optional_boolean_returns_true_if_field_is_yes():
    value = ' yes  '

    result = data_validation_service.clean_optional_boolean(value, 'signed')

    assert result == True

def test_clean_optional_boolean_returns_false_if_field_is_no():
    value = ' no  '

    result = data_validation_service.clean_optional_boolean(value, 'signed')

    assert result == False

def test_clean_optional_boolean_returns_false_if_field_is_none():
    value = None

    result = data_validation_service.clean_optional_boolean(value, 'signed')

    assert result == False

def test_clean_optional_boolean_raises_error_if_field_is_not_yes_or_no_or_none():
    value = ' abc'

    with pytest.raises(ValueError):
        data_validation_service.clean_optional_boolean(value, 'signed')


# Test the function clean_date

def test_clean_optional_date_returns_cleaned_date():
    value = '02/02/2022'
    
    result = data_validation_service.clean_optional_date(value, 'start_date')

    assert result == date(2022, 2, 2)

def test_clean_optional_date_returns_none_if_value_is_none():
    value = None

    result = data_validation_service.clean_optional_date(value, 'start_date')

    assert result == None

def test_clean_optional_date_returns_none_if_value_is_empty_string():
    value = '  '

    result = data_validation_service.clean_optional_date(value, 'start_date')

    assert result == None

def test_clean_optional_date_raises_error_if_value_invalid_format():
    value = '  02- 05-1996 '

    with pytest.raises(ValueError):
        data_validation_service.clean_optional_date(value, 'start_date')


# Test the function clean_role

def test_clean_role_returns_management():
    value = ' management  '

    result = data_validation_service.clean_role(value)

    assert result == 'management'

def test_clean_role_returns_support():
    value = ' support  '

    result = data_validation_service.clean_role(value)

    assert result == 'support'

def test_clean_role_returns_sales():
    value = ' sales  '

    result = data_validation_service.clean_role(value)

    assert result == 'sales'

def test_clean_role_raises_error_if_value_is_none():
    value = None

    with pytest.raises(ValueError):
        data_validation_service.clean_role(value)

def test_clean_role_raises_error_if_value_is_empty():
    value = '  '

    with pytest.raises(ValueError):
        data_validation_service.clean_role(value)

def test_clean_role_raises_error_if_value_is_invalid():
    value = ' abc '

    with pytest.raises(ValueError):
        data_validation_service.clean_role(value)
