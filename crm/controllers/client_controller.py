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
            return 'user_not_authenticated'
        
        clients = self.client_repository.get_all()
        return clients
    
    def get_client(self, client_id):
        '''Return a client. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        client = self.client_repository.get_by_id(client_id)
        return client

    def create_client(self, last_name, first_name,
                      email, phone_number=None, company_name=None):
        '''
        Return new client data after saving in database.
        User must be authenticated and have the role "sales".
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        if not has_role(payload, 'sales'):
            return 'user_not_sales_role'
        
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

    def update_client(self, client_id, last_name=None, first_name=None,
                      email=None, phone_number=None, company_name=None):
        '''
        Returns updated client data after saving in database.
        User must be authenticated and be the client's sales contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        if not has_role(payload, 'sales'):
            return 'user_not_sales_role'
        
        client = self.client_repository.get_by_id(client_id)
        if client is None:
            return 'client_not_found'
        
        if client.sales_contact_id != int(payload['sub']):
            return 'user_not_client_contact' # not contact of client
        
        updates = {}

        if last_name is not None:
            updates['last_name'] = clean_required_string(last_name, 'last_name')
        
        if first_name is not None:
            updates['first_name'] = clean_required_string(first_name, 'first_name')

        if email is not None:
            updates['email'] = clean_email(email)
        
        if phone_number is not None:
            updates['phone_number'] = clean_optional_string(phone_number)
        
        if company_name is not None:
            updates['company_name'] = clean_optional_string(company_name)
        
        updated_client = self.client_repository.update_object(
            object_id=client.id,
            updates=updates
        )

        return updated_client
