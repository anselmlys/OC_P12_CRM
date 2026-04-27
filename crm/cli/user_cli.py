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


@users.command('list')
def get_users():
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

    finally:
        session.close()


@users.command('update')
@click.option('--id', 'user_id', type=int, required=True)
@click.option('--email', type=str, required=False)
@click.option('--last-name', type=str, required=False)
@click.option('--first-name', type=str, required=False)
@click.option('--role', type=str, required=False)
def update_user(user_id, email, last_name, first_name, role):
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

    except ValueError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
