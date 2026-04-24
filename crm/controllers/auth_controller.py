from crm.services import auth_service
from crm.services.password_service import verify_password, hash_password
from crm.services.authorization_service import is_authenticated
from crm.services.data_validation_service import clean_password


class AuthController:
    '''Handle authentication-related operations.'''

    def __init__(self, session, user_repository):
        self.session = session
        self.user_repository = user_repository
    
    def login(self, email, password_entered):
        '''Authenticate a user and return True if login succeeds.'''
        return auth_service.login(self.session, email, password_entered)
    
    def logout(self):
        '''Log out the current user'''
        auth_service.logout()
    
    def change_password(self, old_password_entered, new_password_entered):
        '''Change the current user's password if the old password is valid.'''
        payload = auth_service.get_current_user_payload()

        if not is_authenticated(payload):
            return False
        
        user_id = int(payload['sub'])
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            return False
        
        is_valid = verify_password(old_password_entered, user.hashed_password)
        if not is_valid:
            return False
        
        new_password_entered = clean_password(new_password_entered)

        hashed_password = hash_password(new_password_entered)

        return self.user_repository.update_password(user.id, hashed_password)
