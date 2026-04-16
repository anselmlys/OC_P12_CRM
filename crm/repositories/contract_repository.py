from crm.models.contract import Contract
from crm.repositories.base_repository import BaseRepository


class ContractRepository(BaseRepository):
    '''Repository responsible for db access for Contract objects.'''
    model = Contract
    editable_fields = {
        'client_id',
        'total_amount',
        'remaining_amount',
        'signed',
    }
