from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated


class ContractController:
    '''Handle contract-related operations with authentication and authorization checks.'''
    
    def __init__(self, contract_repository):
        self.contract_repository = contract_repository
    
    def get_all_contracts(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            # Add redirection to login
            return None
        contracts = self.contract_repository.get_all()
        # Modify to add view
        return contracts
