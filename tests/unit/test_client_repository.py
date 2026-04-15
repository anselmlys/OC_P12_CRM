# Test the method get_all

def test_get_all_returns_list_of_clients(client_repo, client_1, client_2):
    result = client_repo.get_all()

    assert len(result) == 2
    assert result[0].first_name == 'Jane'


def test_get_all_returns_empty_list_if_client_not_found(client_repo):
    result = client_repo.get_all()

    assert result == []
