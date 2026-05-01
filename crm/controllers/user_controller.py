from crm.services.auth_service import create_user, get_current_user_payload
from crm.services.authorization_service import is_authenticated, has_role
from crm.services.data_validation_service import (clean_email,
                                                  clean_required_string,
                                                  clean_role,
                                                  clean_password)


class UserController:
    '''Handle user-related operations with authentication and authorization checks.'''

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, email, last_name, first_name, role, password_entered):
        '''
        Return new user data after saving in database.
        User using method must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        email = clean_email(email)
        last_name = clean_required_string(last_name, 'last_name')
        first_name = clean_required_string(first_name, 'first_name')
        role = clean_role(role)
        password_entered = clean_password(password_entered)

        user = create_user(
            user_repository=self.user_repository,
            email=email,
            last_name=last_name,
            first_name=first_name,
            password_entered=password_entered,
            role=role
        )

        return user

    def get_all_users(self):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        users = self.user_repository.get_all()
        return users

    def get_user_by_email(self, email):
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        user = self.user_repository.get_by_email(email)
        return user

    def update_user_by_id(self, user_id, email=None, last_name=None,
                          first_name=None, role=None):
        '''
        Update data of a specific user, save in database then return it.
        User using method must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        updates = {}

        if email is not None:
            updates['email'] = clean_email(email)

        if last_name is not None:
            updates['last_name'] = clean_required_string(last_name, 'last_name')

        if first_name is not None:
            updates['first_name'] = clean_required_string(first_name, 'first_name')

        if role is not None:
            updates['role'] = clean_role(role)

        user = self.user_repository.update_object(user_id, updates)
        return user

    def delete_user_by_id(self, user_id):
        '''
        Delete a specific user from the database and return True.
        User using method must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        return self.user_repository.delete_object(user_id)
