from sqlalchemy.exc import SQLAlchemyError

from crm.models.client import Client


class ClientRepository:
    '''Repository responsible for db access for Client objects.'''

    def __init__(self, session):
        self.session = session
    
    def get_all(self):
        try:
            return self.session.query(Client).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching client data') from e
