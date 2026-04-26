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
    init_db()
    cli()
