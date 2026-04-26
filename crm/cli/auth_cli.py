import click

from crm.db import Session
from crm.repositories.user_repository import UserRepository
from crm.controllers.auth_controller import AuthController


@click.group()
def auth():
    '''Manage authentication.'''
    pass


@auth.command('login')
@click.option('--email', type=str, required=True)
@click.password_option()
def login(email, password):
    session = Session()

    try:
        user_repository = UserRepository(session)
        auth_controller = AuthController(session, user_repository)

        result = auth_controller.login(email, password)

        if result == 'user_not_found':
            click.secho('User not found.', fg='red')
            return
        
        elif result == 'invalid_password':
            click.secho('Password invalid.', fg='red')
            return
        
        else:
            click.secho('Login successful!', fg='green')

    finally:
        session.close()
