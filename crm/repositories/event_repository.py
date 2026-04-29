from sqlalchemy.exc import SQLAlchemyError

from crm.models.event import Event
from crm.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository):
    '''Repository responsible for db access for Event objects.'''
    model = Event
    editable_fields = {
        'contract_id',
        'start_date',
        'end_date',
        'support_contact_id',
        'location',
        'number_of_attendees',
        'notes',
    }

    def create_event(self, contract_id,
                     start_date=None, end_date=None,
                     support_contact_id=None, location=None,
                     number_of_attendees=None, notes=None):
        '''Create and save a new event then return it.'''
        event = Event(
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            support_contact_id=support_contact_id,
            location=location,
            number_of_attendees=number_of_attendees,
            notes=notes
        )

        try:
            self.session.add(event)
            self.session.commit()
            self.session.refresh(event)
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while saving event data') from e

        return event

    def get_events_without_support_contact(self):
        '''Return a list of all events to which no support contact has been assigned.'''
        try:
            events = self.session.query(Event).filter(Event.support_contact_id == None).all()
            return events

        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching {self.model.__name__} data') from e
        
    def get_events_by_support_contact_id(self, user_id):
        '''Filter events based on a support contact id and return the list.'''
        try:
            events = self.session.query(Event).filter(Event.support_contact_id == user_id).all()
            return events
        
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching {self.model.__name__} data') from e

    def update_support_contact(self, event, new_support_contact_id):
        '''Update the support contact of an event, then return the updated event.'''
        try:
            event.support_contact_id = new_support_contact_id
            
            self.session.commit()
            self.session.refresh(event)

            return event
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while updating {self.model.__name__} data') from e
