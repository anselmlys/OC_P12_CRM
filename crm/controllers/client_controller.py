from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated, has_role
from crm.services.data_validation_service import (clean_required_string,
                                                  clean_optional_string,
                                                  clean_email)


class ClientController:
    '''Handle client-related operations with authentication and authorization checks.'''

    def __init__(self, client_repository):
        self.client_repository = client_repository
    
    def get_all_clients(self):
        '''Return a list of all clients. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return None
        
        clients = self.client_repository.get_all()
        return clients

    def create_client(self, last_name, first_name,
                      email, phone_number=None, company_name=None):
        '''
        Return new client data after saving in database.
        User must be authenticated and have the role "sales".
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return None
        
        if not has_role(payload, 'sales'):
            return None
        
        last_name = clean_required_string(last_name, 'last_name')
        first_name = clean_required_string(first_name, 'first_name')
        email = clean_email(email)
        phone_number = clean_optional_string(phone_number)
        company_name = clean_optional_string(company_name)
        
        client = self.client_repository.create_client(
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            sales_contact_id=int(payload['sub'])
        )

        return client
