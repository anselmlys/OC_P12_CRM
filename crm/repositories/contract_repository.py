from sqlalchemy.exc import SQLAlchemyError

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

    def create_contract(self, client_id, total_amount=None,
                        remaining_amount=None, signed=False):
        '''Create and save a new contract then return it.'''
        contract = Contract(
            client_id=client_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=signed,
        )

        try:
            self.session.add(contract)
            self.session.commit()
            self.session.refresh(contract)

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while saving contract data') from e
        
        return contract
    
    def get_unsigned_contracts(self):
        try:
            contracts = self.session.query(Contract).filter(Contract.signed == False).all()
            return contracts
        
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while saving contract data') from e
