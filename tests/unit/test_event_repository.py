# Test the method get_all

def test_get_all_returns_list_of_events(event_repo, event_1, event_2):
    result = event_repo.get_all()

    assert len(result) == 2
    assert result[0].contract_id == 1


def test_get_all_returns_empty_list_if_no_event_found(event_repo):
    result = event_repo.get_all()

    assert result == []
