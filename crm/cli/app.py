import click

from crm.cli.auth_cli import auth
from crm.cli.user_cli import users


@click.group()
def cli():
    '''EpicEvents CRM command line interface.'''
    pass


cli.add_command(auth)
cli.add_command(users)
