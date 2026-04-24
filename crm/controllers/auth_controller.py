from crm.services import auth_service


class AuthController:
    '''Handle authentication-related operations.'''

    def __init__(self, session):
        self.session = session
    
    def login(self, email, password_entered):
        '''Authenticate a user and return True if login succeeds.'''
        result = auth_service.login(self.session, email, password_entered)
        return result
    
    def logout(self):
        '''Log out the current user'''
        auth_service.logout()
