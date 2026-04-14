from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated


class ClientController:
    '''Handle client-related operations with authentication and authorization checks.'''

    def __init__(self, client_repository):
        self.client_repository = client_repository
    
    def get_all_clients(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            # Add redirection to login
            return None
        clients = self.client_repository.get_all()
        # Modify to add view
        return clients
            
