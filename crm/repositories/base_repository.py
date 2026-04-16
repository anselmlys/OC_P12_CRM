from abc import ABC
from sqlalchemy.exc import SQLAlchemyError


class BaseRepository(ABC):
    '''Repository responsible for db access for objects.'''
    model = None
    editable_fields = {}

    def __init__(self, session):
        self.session = session

    def get_all(self):
        '''Return a list of all objects.'''
        try:
            objects = self.session.query(self.model).all()
            return objects
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching {self.model.__name__} data') from e

    def get_by_id(self, object_id):
        '''Return a object by ID or None if not found.'''
        try:
            obj = self.session.query(self.model).filter(self.model.id == object_id).first()
            return obj
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database error while fetching {self.model.__name__} data') from e

    def update_object(self, object_id, updates):
        '''
        Update multiple fields of an object and return the updated object
        or None if not found.
        '''
        try:
            obj = self.get_by_id(object_id)
            if obj is None:
                return None
            for field, value in updates.items():
                if field not in self.editable_fields:
                    raise ValueError(f'Field "{field}" cannot be updated')
                setattr(obj, field, value)
            
            self.session.commit()
            self.session.refresh(obj)

            return obj
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while updating {self.model.__name__} data') from e

    def delete_object(self, object_id):
        '''Delete an object by ID and return True if deleted else False.'''
        try:
            obj = self.get_by_id(object_id)
            if obj is None:
                return False
            
            self.session.delete(obj)
            self.session.commit()

            return True
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f'Database error while deleting {self.model.__name__} data') from e
