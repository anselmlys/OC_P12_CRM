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
