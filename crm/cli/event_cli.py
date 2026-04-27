import click

from crm.db import Session
from crm.repositories.user_repository import UserRepository
from crm.repositories.event_repository import EventRepository
from crm.controllers.event_controller import EventController


@click.group()
def events():
    '''Manage events.'''
    pass


@events.command('list')
def list_events():
    '''Display all events.'''
    session = Session()

    try:
        user_repository = UserRepository(session)
        event_repository = EventRepository(session)
        event_controller = EventController(event_repository, user_repository)

        result = event_controller.get_all_events()

        if result is None:
            click.echo('Please login first.')
            return
        
        if not result:
            click.echo('No events found.')
        
        for event in result:
            click.echo(
                f'Event ID: {event.id}'
                f'Contract ID: {event.contract_id}'
                f'Client name: {event.contract.client.first_name} {event.contract.client.last_name}'
                f'Client contact: {event.contract.client.email} | {event.contract.client.phone_number}'
                f'Start date: {event.start_date}'
                f'End date: {event.end_date}'
                f'Support contact: {event.support_contact.first_name} {event.support_contact.last_name}'
                f'Location: {event.location}'
                f'Attendees: {event.number_of_attendees}'
                f'Notes: {event.notes}'
            )

    finally:
        session.close()
