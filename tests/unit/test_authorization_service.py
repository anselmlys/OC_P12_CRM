from crm.services import authorization_service


# Test the function is_authenticated
def test_is_authenticated_returns_true_if_payload_not_none():
    test_payload = {}

    result = authorization_service.is_authenticated(test_payload)

    assert result is True


def test_is_authenticated_returns_false_if_payload_is_none():
    test_payload = None

    result = authorization_service.is_authenticated(test_payload)

    assert result is False


# Test the function has_role

def test_has_role_returns_true_if_role_in_payload():
    test_payload = {'role': 'sales'}

    result = authorization_service.has_role(test_payload, 'sales')

    assert result is True


def test_has_role_returns_false_if_role_not_in_payload():
    test_payload = {'role': 'management'}

    result = authorization_service.has_role(test_payload, 'sales')

    assert result is False


def test_has_role_returns_false_if_payload_is_none():
    test_payload = None

    result = authorization_service.has_role(test_payload, 'sales')

    assert result is False
