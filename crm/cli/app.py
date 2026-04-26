import click

from crm.cli.auth_cli import auth


@click.group()
def cli():
    '''EpicEvents CRM command line interface.'''
    pass


cli.add_command(auth)
