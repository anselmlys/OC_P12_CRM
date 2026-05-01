import sentry_sdk
import click

from crm.sentry_config import init_sentry
from crm.cli.app import cli


def main():
    '''Initialize the app and prepare the main execution flow.'''
    init_sentry()

    try:
        cli()

    # All unhandled errors will be sent to Sentry
    except Exception as e:
        sentry_sdk.capture_exception(e)
        click.secho('Unexpected error has occurred.', fg='red')
