import click

from crm.db import Session
from crm.repositories.user_repository import UserRepository
from crm.controllers.user_controller import UserController


@click.group()
def users():
    '''Manage users.'''
    pass


@users.command('create-user')
@click.option('--email', type=str, required=True)
@click.option('--last-name', type=str, required=True)
@click.option('--first-name', type=str, required=True)
@click.option('--role', type=str, required=True)
@click.password_option()
def create_user(email, last_name, first_name, role, password):
    session = Session()

    try:
        user_repository = UserRepository(session)
        user_controller = UserController(user_repository)

        result = user_controller.create_user(email, last_name, first_name, role, password)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        else:
            click.secho('User successfully created.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
