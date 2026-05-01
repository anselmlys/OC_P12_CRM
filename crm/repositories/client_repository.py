from sqlalchemy.exc import SQLAlchemyError

from crm.models.client import Client
from crm.repositories.base_repository import BaseRepository


class ClientRepository(BaseRepository):
    '''Repository responsible for db access for Client objects.'''
    model = Client
    editable_fields = {
        'last_name',
        'first_name',
        'email',
        'phone_number',
        'company_name',
        'sales_contact_id',
    }

    def create_client(self, last_name, first_name, email, phone_number=None,
                      company_name=None, sales_contact_id=None):
        '''Create and save a new client then return it.'''
        client = Client(
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            sales_contact_id=sales_contact_id
        )
        try:
            self.session.add(client)
            self.session.commit()
            self.session.refresh(client)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError('Database error while saving client data') from e

        return client
