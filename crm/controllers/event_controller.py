from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated, has_role
from crm.services.data_validation_service import (clean_optional_date,
                                                  clean_optional_string,
                                                  clean_optional_integer,) 


class EventController:
    '''Handle event-related operations with authentication and authorization checks.'''

    def __init__(self, event_repository, contract_repository, user_repository):
        self.event_repository = event_repository
        self.contract_repository = contract_repository
        self.user_repository = user_repository

    def get_all_events(self):
        '''Return a list of all events. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        events = self.event_repository.get_all()
        return events
    
    def get_event(self, event_id):
        '''Return an event. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        event = self.event_repository.get_by_id(event_id)
        return event
    
    def get_events_to_assign(self):
        '''
        Retrieve all events without a support contact.
        User must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        if not has_role(payload, 'management'):
            return 'user_not_management_role'
        
        events = self.event_repository.get_events_without_support_contact()
        return events
    
    def get_assigned_events(self):
        '''
        Retrieve all events assigned to the user.
        User must be authenticated and have the role "support".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        if not has_role(payload, 'support'):
            return 'user_not_support_role'
        
        events = self.event_repository.get_events_by_support_contact_id(int(payload['sub']))
        return events
    
    def create_event(self, contract_id,
                     start_date=None, end_date=None,
                     support_contact_id=None, location=None,
                     number_of_attendees=None, notes=None):
        '''
        Return updated contract after saving in database.
        User must be authenticated and be the client's sales contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        contract = self.contract_repository.get_by_id(contract_id)
        if contract is None:
            return 'contract_not_found'

        if contract.client.sales_contact_id != int(payload['sub']):
            return 'user_not_client_contact'
        
        if not contract.signed:
            return 'contract_not_signed'
        
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
    
    def assign_support_contact(self, event_id, support_contact_id):
        '''
        Update the support contact of an event and returns the updated event.
        User must be authenticated and have the role "management".
        New support contact must be a user with the role "support".
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        if not has_role(payload, 'management'):
            return 'user_not_management_role'
        
        support_contact = self.user_repository.get_by_id(support_contact_id)
        if support_contact is None:
            return 'support_contact_not_found'
        
        if support_contact.role != 'support':
            return 'support_contact_not_support_role'
        
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            return 'event_not_found'

        event = self.event_repository.update_support_contact(
            event,
            support_contact.id
        )

        return event
    
    def update_event(self, event_id, start_date=None, end_date=None,
                     location=None, number_of_attendees=None, notes=None):
        '''
        Return updated event after saving the modifications.
        User must be authenticated and be the support contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'
        
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            return 'event_not_found'
        
        if event.support_contact_id != int(payload['sub']):
            return 'user_not_client_support_contact'
        
        start_date = clean_optional_date(start_date, 'start_date')
        end_date = clean_optional_date(end_date, 'end_date')
        location = clean_optional_string(location)
        number_of_attendees = clean_optional_integer(number_of_attendees, 'number_of_attendees')
        notes = clean_optional_string(notes)

        updates = {
            'start_date': start_date,
            'end_date': end_date,
            'location': location,
            'number_of_attendees': number_of_attendees,
            'notes': notes,
        }

        updated_event = self.event_repository.update_object(event_id, updates)

        return updated_event
