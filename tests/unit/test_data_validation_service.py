import pytest

from crm.services import data_validation_service


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
