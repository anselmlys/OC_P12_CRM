from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated
from crm.services.data_validation_service import (clean_optional_date,
                                                  clean_optional_string,
                                                  clean_optional_integer) 


class EventController:
    '''Handle event-related operations with authentication and authorization checks.'''

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def get_all_events(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return None
        
        events = self.event_repository.get_all()
        return events
    
    def create_event(self, contract,
                     start_date=None, end_date=None,
                     support_contact_id=None, location=None,
                     number_of_attendees=None, notes=None):
        '''
        Return updated contract after saving in database.
        User must be authenticated and be the client's sales contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return None
        
        if contract.client.sales_contact_id != int(payload['sub']):
            return None
        
        if not contract.signed:
            return None
        
        start_date = clean_optional_date(start_date, 'start_date')
        end_date = clean_optional_date(end_date, 'end_date')
        support_contact_id = clean_optional_integer(support_contact_id, 'support_contact_id')
        location = clean_optional_string(location)
        number_of_attendees = clean_optional_integer(number_of_attendees, 'number_of_attendees')
        notes = clean_optional_string(notes)
        
        event = self.event_repository.create_event(
            contract_id=contract.id,
            start_date=start_date,
            end_date=end_date,
            support_contact_id=support_contact_id,
            location=location,
            number_of_attendees=number_of_attendees,
            notes=notes,
        )

        return event
