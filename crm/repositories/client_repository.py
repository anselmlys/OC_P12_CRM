from sqlalchemy.exc import SQLAlchemyError

from crm.models.client import Client


class ClientRepository:
    '''Repository responsible for db access for Client objects.'''

    def __init__(self, session):
        self.session = session
    
    def get_all(self):
        '''Return a list of all clients.'''
        try:
            clients = self.session.query(Client).all()
            return clients
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching client data') from e

    def get_by_id(self, client_id):
        '''Return a client by ID, or None if not found.'''
        try:
            client = self.session.query(Client).filter(Client.id == client_id).first()
            return client
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching client data') from e

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
        try :
            self.session.add(client)
            self.session.commit()
            self.session.refresh(client)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while saving client data') from e

        return client

    def update_client(self, client_id, updates):
        '''
        Update multiple fields of a client and return the updated client,
        or None if not found.
        '''
        try:
            client = self.get_by_id(client_id)
            if client is None:
                return None
            
            allowed_fields = {
                "last_name",
                "first_name",
                "email",
                "phone_number",
                "company_name",
                "sales_contact_id",
            }

            for field, value in updates.items():
                if field not in allowed_fields:
                    raise ValueError(f'Field "{field}" cannot be updated')
                setattr(client, field, value)

            self.session.commit()
            self.session.refresh(client)

            return client
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while updating client data') from e

    def delete_client(self, client_id):
        '''Delete a client by ID and return True if deleted else False.'''
        try:
            client = self.get_by_id(client_id)
            if client is None:
                return False
            
            self.session.delete(client)
            self.session.commit()

            return True
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while deleting client data') from e
