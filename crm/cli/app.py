import click

from crm.cli.db_cli import db
from crm.cli.auth_cli import auth
from crm.cli.user_cli import users
from crm.cli.client_cli import clients
from crm.cli.contract_cli import contracts
from crm.cli.event_cli import events


@click.group()
def cli():
    '''EpicEvents CRM command line interface.'''
    pass


cli.add_command(db)
cli.add_command(auth)
cli.add_command(users)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)
