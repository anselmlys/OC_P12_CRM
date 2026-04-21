from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated, has_role
from crm.services.data_validation_service import (clean_optional_integer,
                                                  clean_required_integer,
                                                  clean_optional_boolean)


class ContractController:
    '''Handle contract-related operations with authentication and authorization checks.'''
    
    def __init__(self, contract_repository):
        self.contract_repository = contract_repository
    
    def get_all_contracts(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return None
        
        contracts = self.contract_repository.get_all()
        return contracts
    
    def create_contract(self, client_id, total_amount=None,
                        remaining_amount=None, signed=False):
        '''
        Return new contract data after saving in database.
        User must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return None
        
        if not has_role(payload, 'management'):
            return None

        client_id = clean_required_integer(client_id, 'client_id')
        total_amount = clean_optional_integer(total_amount, 'total_amount')
        remaining_amount = clean_optional_integer(remaining_amount, 'remaining_amount')
        signed = clean_optional_boolean(signed, 'signed')

        contract = self.contract_repository.create_contract(
            client_id=client_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=signed,
        )

        return contract

    def update_contract(self, contract, client_id, total_amount=None,
                        remaining_amount=None, signed=False):
        '''
        Return updated contract after saving in database.
        User must be authenticated and have the role "management"
        or be the client's sales contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return None
        
        if (
            not has_role(payload, 'management')
            and payload['sub'] != str(contract.client.sales_contact_id)
        ):
            return None
        
        client_id = clean_required_integer(client_id, 'client_id')
        total_amount = clean_optional_integer(total_amount, 'total_amount')
        remaining_amount = clean_optional_integer(remaining_amount, 'remaining_amount')
        signed = clean_optional_boolean(signed, 'signed')

        updates = {
            'client_id': client_id,
            'total_amount': total_amount,
            'remaining_amount': remaining_amount,
            'signed': signed,
        }

        updated_contract = self.contract_repository.update_object(contract.id, updates)

        return updated_contract
