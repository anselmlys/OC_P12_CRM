from sqlalchemy.exc import SQLAlchemyError

from crm.models.user import User
from crm.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    '''Repository responsible for db access for User objects.'''
    model = User
    editable_fields = {
        'email',
        'last_name',
        'first_name',
        'role',
    }

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
    
    def get_by_email(self, email):
        '''Return a user by email or None if not found.'''
        try:
            user = self.session.query(User).filter(User.email == email).first()
            return user
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching user with email') from e
