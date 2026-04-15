# Test the method get_all

def test_get_all_returns_list_of_contracts(contract_repo, contract_1, contract_2):
    result = contract_repo.get_all()

    assert len(result) == 2
    assert result[0].client_id == 1


def test_get_all_returns_empty_list_if_contract_not_found(contract_repo):
    result = contract_repo.get_all()

    assert result == []
