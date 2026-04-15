from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated


class EventController:
    '''Handle event-related operations with authentication and authorization checks.'''

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def get_all_events(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            # Add redirection to login
            return None
        events = self.event_repository.get_all()
        # Modify to add view 
        return events
