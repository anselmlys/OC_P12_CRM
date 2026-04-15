from sqlalchemy.exc import SQLAlchemyError

from crm.models.event import Event


class EventRepository:
    '''Repository responsible for db access for Event objects.'''

    def __init__(self, session):
        self.session = session

    def get_all(self):
        try:
            events = self.session.query(Event).all()
            return events
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching client data') from e
