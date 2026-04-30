import sentry_sdk
import click

from crm.sentry_config import init_sentry
from crm.db import engine, Session
from crm.models.base import Base
from crm.cli.app import cli

from crm.models.user import User
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.event import Event


def init_db():
    '''Create tables in database if they do not already exist.'''
    Base.metadata.create_all(engine)


def main():
    '''Initialize the app and prepare the main execution flow.'''
    init_sentry()
    init_db()

    try:
        cli()

    # All unhandled errors will be sent to Sentry
    except Exception as e:
        sentry_sdk.capture_exception(e)
        click.secho('Unexpected error has occurred.', fg='red')
