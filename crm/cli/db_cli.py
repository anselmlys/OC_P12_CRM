import click

from crm.db import engine, Session
from crm.models.base import Base
from crm.models.user import User
from crm.models.client import Client  # noqa: F401
from crm.models.contract import Contract  # noqa: F401
from crm.models.event import Event  # noqa: F401
from crm.repositories.user_repository import UserRepository
from crm.services.auth_service import create_user
from crm.services.data_validation_service import (clean_email,
                                                  clean_required_string,
                                                  clean_password)


@click.group()
def db():
    '''Manage database setup.'''
    pass


@db.command('init')
def init_db():
    '''Create database tables if they do not already exist.'''
    Base.metadata.create_all(engine)
    click.secho('Database initialized successfully.', fg='green')


@db.command('create-admin')
@click.option('--email', type=str, required=True)
@click.option('--last-name', type=str, required=True)
@click.option('--first-name', type=str, required=True)
@click.password_option()
def create_admin(email, last_name, first_name, password):
    '''Create the first management user if no user exists.'''
    session = Session()

    try:
        user_count = session.query(User).count()

        if user_count > 0:
            click.secho('Admin creation refused: user already exists.', fg='red')
            return

        user_repository = UserRepository(session)

        email = clean_email(email)
        last_name = clean_required_string(last_name, 'last_name')
        first_name = clean_required_string(first_name, 'first_name')
        password = clean_password(password)

        create_user(
            user_repository=user_repository,
            email=email,
            last_name=last_name,
            first_name=first_name,
            password_entered=password,
            role='management'
        )

        click.secho('First management user created successfully.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
