from sqlalchemy.exc import SQLAlchemyError

from crm.models.user import User


class UserRepository:
    '''Repository responsible for db access for User objects.'''

    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        '''Return a user by email or None if not found.'''
        try:
            return self.session.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching user with email') from e

    def create_user(self, email, last_name, first_name, hashed_password, role):
        '''Create and save a new user to the db.'''
        user = User(email=email, last_name=last_name, first_name=first_name,
                    hashed_password=hashed_password, role=role)
        
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError('Database error while creating user') from e
