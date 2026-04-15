from sqlalchemy.exc import SQLAlchemyError

from crm.models.contract import Contract


class ContractRepository:
    '''Repository responsible for db access for Contract objects.'''

    def __init__(self, session):
        self.session = session

    def get_all(self):
        try:
            return self.session.query(Contract).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching client data') from e
