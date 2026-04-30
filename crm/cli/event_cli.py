import sentry_sdk
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from crm.db import Session
from crm.repositories.user_repository import UserRepository
from crm.repositories.contract_repository import ContractRepository
from crm.repositories.event_repository import EventRepository
from crm.controllers.event_controller import EventController


@click.group()
def events():
    '''Manage events.'''
    pass


@events.command('create')
@click.option('--contract-id', type=int, required=True)
@click.option('--start-date', help='Format: (DD/MM/YYYY)', type=str, required=False)
@click.option('--end-date', help='Format: (DD/MM/YYYY)', type=str, required=False)
@click.option('--support-contact-id', type=int, required=False)
@click.option('--location', type=str, required=False)
@click.option('--number-of-attendees', type=int, required=False)
@click.option('--notes', type=str, required=False)
def create_event(contract_id, start_date, end_date, support_contact_id,
                 location, number_of_attendees, notes):
    '''Create a new event.'''
    sentry_sdk.set_tag('command', 'events.create')
    sentry_sdk.set_tag('domain', 'events')

    session = Session()

    try:
        event_repository = EventRepository(session)
        user_repository = UserRepository(session)
        contract_repository = ContractRepository(session)
        event_controller = EventController(
            event_repository,
            contract_repository,
            user_repository
        )

        result = event_controller.create_event(
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            support_contact_id=support_contact_id,
            location=location,
            number_of_attendees=number_of_attendees,
            notes=notes
        )

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'contract_not_found':
            click.secho('The contract was not found.', fg='red')
            return
        
        elif result == 'user_not_client_contact':
            click.secho('You are not the contact of this client.', fg='red')
            return
        
        elif result == 'contract_not_signed':
            click.secho('The contract is not signed yet.', fg='red')
            return
        
        else:
            click.secho('Event successfully created.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@events.command('list')
@click.option('--to-assign', is_flag=True, help='Show only events not assigned to a support contact.')
@click.option('--assigned', is_flag=True, help='Show only events assigned to you.')
def get_events(to_assign, assigned):
    '''List all events.'''
    session = Session()

    try:
        user_repository = UserRepository(session)
        contract_repository = ContractRepository(session)
        event_repository = EventRepository(session)
        event_controller = EventController(
            event_repository,
            contract_repository,
            user_repository
        )

        if to_assign:
            result = event_controller.get_events_to_assign()

        elif assigned:
            result = event_controller.get_assigned_events()

        else:
            result = event_controller.get_all_events()

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        elif result == 'user_not_support_role':
            click.secho('Action restricted to the support team.', fg='red')
            return
        
        else:
            console = Console()

            table = Table(title='Events', show_lines=True)

            table.add_column('ID', justify='right', no_wrap=True)
            table.add_column('Client ID', justify='left', no_wrap=True)
            table.add_column('Client', justify='left', no_wrap=True)
            table.add_column('Contract ID', justify='left', no_wrap=True)
            table.add_column('Support ID', justify='left', no_wrap=True)
            table.add_column('Support', justify='left', no_wrap=True)

            for event in result:
                support_contact_id = event.support_contact_id or '-'
                if event.support_contact:
                    support_contact_first_name = event.support_contact.first_name.title()
                    support_contact_last_name = event.support_contact.last_name.title()
                else:
                    support_contact_first_name = '-'
                    support_contact_last_name = '-'

                table.add_row(
                    str(event.id),
                    str(event.contract.client.id),
                    f'{event.contract.client.first_name.title()} {event.contract.client.last_name.title()}',
                    str(event.contract.id),
                    str(support_contact_id),
                    f'{support_contact_first_name} {support_contact_last_name}'
                )
            
            console.print(table)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@events.command('detail')
@click.option('--id', 'event_id', type=int, required=True)
def get_event(event_id):
    '''Display an event's details using its id.'''
    session = Session()

    try:
        user_repository = UserRepository(session)
        contract_repository = ContractRepository(session)
        event_repository = EventRepository(session)
        event_controller = EventController(
            event_repository,
            contract_repository,
            user_repository
        )
        
        result = event_controller.get_event(event_id)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        else:
            console = Console()

            start_date = (
                result.start_date.strftime('%d/%m/%Y %H:%M')
                if result.start_date
                else '-'
            )

            end_date = (
                result.end_date.strftime('%d/%m/%Y %H:%M')
                if result.end_date
                else '-'
            )

            support_contact = (
                f'{result.support_contact.first_name.title()} {result.support_contact.last_name.title()}'
                if result.support_contact
                else '-'
            )

            client_email = result.contract.client.email or '-'
            client_phone = result.contract.client.phone_number or '-'
            support_contact_id = result.support_contact_id or '-'
            location = result.location or '-'
            attendees = result.number_of_attendees or '-'
            notes = result.notes or '-'

            content = Text()
            content.append(f'ID:                {str(result.id)}\n')
            content.append(f'Contract ID:       {str(result.contract_id)}\n')
            content.append(f'Client ID:         {str(result.contract.client_id)}\n')
            content.append(f'Client:            {result.contract.client.first_name.title()} {result.contract.client.last_name.title()}\n')
            content.append(f'Client contact:    {client_email}\n{client_phone}\n')
            content.append(f'Start date:        {start_date}\n')
            content.append(f'End date:          {end_date}\n')
            content.append(f'Support ID:        {support_contact_id}\n')
            content.append(f'Support contact:   {support_contact}\n')
            content.append(f'Location:          {location}\n')
            content.append(f'Attendees:         {attendees}')
            content.append(f'Notes:             {notes}')

            panel = Panel(
                content,
                title=f'Event #{result.id}'
            )
            
            console.print(panel)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@events.command('update')
@click.option('--id', 'event_id', type=int, required=True)
@click.option('--start-date', help='Format: (DD/MM/YYYY)', type=str, required=False)
@click.option('--end-date', help='Format: (DD/MM/YYYY)', type=str, required=False)
@click.option('--location', type=str, required=False)
@click.option('--number-of-attendees', type=int, required=False)
@click.option('--notes', type=str, required=False)
def update_event(event_id, start_date, end_date,
                 location, number_of_attendees, notes):
    '''Update an event by id.'''
    sentry_sdk.set_tag('command', 'events.update')
    sentry_sdk.set_tag('domain', 'events')

    session = Session()

    try:
        event_repository = EventRepository(session)
        user_repository = UserRepository(session)
        contract_repository = ContractRepository(session)
        event_controller = EventController(
            event_repository,
            contract_repository,
            user_repository
        )

        result = event_controller.update_event(
            event_id=event_id,
            start_date=start_date,
            end_date=end_date,
            location=location,
            number_of_attendees=number_of_attendees,
            notes=notes
        )

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'event_not_found':
            click.secho('The event was not found.', fg='red')
            return
        
        elif result == 'user_not_client_support_contact':
            click.secho('You are not the support contact on this event.', fg='red')
            return
        
        else:
            click.secho('Event successfully updated.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@events.command('assign')
@click.option('--id', 'event_id', type=int, required=True)
@click.option('--support-id', 'support_contact_id', type=int, required=True)
def assign_event(event_id, support_contact_id):
    '''Assign a support contact to an event.'''
    session = Session()

    try:
        event_repository = EventRepository(session)
        user_repository = UserRepository(session)
        contract_repository = ContractRepository(session)
        event_controller = EventController(
            event_repository,
            contract_repository,
            user_repository
        )

        result = event_controller.assign_support_contact(event_id, support_contact_id)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        elif result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        elif result == 'support_contact_not_found':
            click.secho('Support contact was not found in users.', fg='red')
            return
        
        elif result == 'support_contact_not_support_role':
            click.secho('User enterred for support contact does not have role "support".', fg='red')
            return
        
        else:
            click.secho('Support contact successfully updated.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
