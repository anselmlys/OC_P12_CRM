import sentry_sdk
import click
from rich.console import Console
from rich.table import Table

from crm.db import Session
from crm.repositories.user_repository import UserRepository
from crm.controllers.user_controller import UserController


@click.group()
def users():
    '''Manage users.'''
    pass


@users.command('create')
@click.option('--email', type=str, required=True)
@click.option('--last-name', type=str, required=True)
@click.option('--first-name', type=str, required=True)
@click.option('--role', type=str, required=True)
@click.password_option()
def create_user(email, last_name, first_name, role, password):
    '''Create new user.'''
    sentry_sdk.set_tag('command', 'users.create')
    sentry_sdk.set_tag('domain', 'users')

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

            # Log user creation in Sentry
            sentry_sdk.capture_message(
                f'User created: {result.id}',
                level='info',
            )

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@users.command('list')
def get_users():
    '''List all the users.'''
    session = Session()

    try:
        user_repository = UserRepository(session)
        user_controller = UserController(user_repository)

        result = user_controller.get_all_users()

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        else:
            console = Console()

            table = Table(title='Users',show_lines=True)

            table.add_column('ID', justify='right', no_wrap=True)
            table.add_column('Email', justify='left', no_wrap=True)
            table.add_column('Last name', justify='left', no_wrap=True)
            table.add_column('First name', justify='left', no_wrap=True)
            table.add_column('Role', justify='left', no_wrap=True)

            for user in result:
                if user.role == 'management':
                    role_display = '[blue]management[/blue]'
                elif user.role == 'sales':
                    role_display = '[red]sales[/red]'
                elif user.role == 'support':
                    role_display= '[green]support[/green]'

                table.add_row(
                    str(user.id),
                    user.email,
                    user.last_name.title(),
                    user.first_name.title(),
                    role_display
                )
            
            console.print(table)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@users.command('update')
@click.option('--id', 'user_id', type=int, required=True)
@click.option('--email', type=str, required=False)
@click.option('--last-name', type=str, required=False)
@click.option('--first-name', type=str, required=False)
@click.option('--role', type=str, required=False)
def update_user(user_id, email, last_name, first_name, role):
    '''Update a user by id.'''
    sentry_sdk.set_tag('command', 'users.update')
    sentry_sdk.set_tag('domain', 'users')

    session = Session()

    try:
        user_repository = UserRepository(session)
        user_controller = UserController(user_repository)

        result = user_controller.update_user_by_id(
            user_id,
            email,
            last_name,
            first_name,
            role
        )

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        else:
            click.secho('User successfully updated.', fg='green')

            # Log user update in Sentry
            sentry_sdk.capture_message(
                f'User updated: {result.id}',
                level='info',
            )

    except ValueError as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@users.command('delete')
@click.option('--id', 'user_id', type=int, required=True)
def delete_user(user_id):
    '''Delete a user by id.'''
    sentry_sdk.set_tag('command', 'users.delete')
    sentry_sdk.set_tag('domain', 'users')

    session = Session()

    try:
        user_repository = UserRepository(session)
        user_controller = UserController(user_repository)

        result = user_controller.delete_user_by_id(user_id)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        else:
            click.secho('User successfully deleted.', fg='green')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
