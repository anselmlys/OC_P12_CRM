import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from crm.db import Session
from crm.repositories.client_repository import ClientRepository
from crm.controllers.client_controller import ClientController


@click.group()
def clients():
    '''Manage clients.'''
    pass


@clients.command('create')
@click.option('--last-name', type=str, required=True)
@click.option('--first-name', type=str, required=True)
@click.option('--email', type=str, required=True)
@click.option('--phone-number', type=str, required=False)
@click.option('--company-name', type=str, required=False)
def create_client(last_name, first_name, email, phone_number, company_name):
    '''Create a new client.'''
    session = Session()

    try:
        client_repository = ClientRepository(session)
        client_controller = ClientController(client_repository)

        result = client_controller.create_client(
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name
        )

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        if result == 'user_not_sales_role':
            click.secho('Action restricted to the sales team.', fg='red')
            return
        
        else:
            click.secho('Client successfully created.', fg='green')
        
    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@clients.command('list')
def get_clients():
    '''List all clients.'''
    session = Session()

    try:
        client_repository = ClientRepository(session)
        client_controller = ClientController(client_repository)

        result = client_controller.get_all_clients()

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        else:
            console = Console()

            table = Table(title='Clients', show_lines=True)

            table.add_column('ID', justify='right', no_wrap=True)
            table.add_column('Name', justify='left', no_wrap=True)
            table.add_column('Email', justify='left', no_wrap=True)
            table.add_column('Company', justify='left', no_wrap=True)
            table.add_column('Sales contact ID', justify='left', no_wrap=True)
            table.add_column('Sales contact', justify='left', no_wrap=True)

            for client in result:
                company_name = client.company_name or '-'
                sales_contact = client.sales_contact or '-'


                table.add_row(
                    str(client.id),
                    f'{client.first_name.title()} {client.last_name.title()}',
                    client.email,
                    company_name.title(),
                    str(client.sales_contact_id),
                    f'{sales_contact.first_name.title()} {sales_contact.last_name.title()}'
                )

            console.print(table)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@clients.command('detail')
@click.option('--id', 'client_id', type=int, required=True)
def get_client(client_id):
    '''Display a client's details using their id.'''
    session = Session()

    try:
        client_repository = ClientRepository(session)
        client_controller = ClientController(client_repository)

        result = client_controller.get_client(client_id)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        else:
            console = Console()

            created_at = result.created_at.strftime('%d/%m/%Y %H:%M')
            updated_at = result.updated_at.strftime('%d/%m/%Y %H:%M')
            phone_number = result.phone_number or '-'
            company_name = result.company_name or '-'
            sales_contact = result.sales_contact or '-'

            content = Text()
            content.append(f'ID:                {str(result.id)}\n')
            content.append(f'Name:              {result.first_name.title()} {result.last_name.title()}\n')
            content.append(f'Email:             {result.email}\n')
            content.append(f'Phone number:      {phone_number}\n')
            content.append(f'Company name:      {company_name.title()}\n')
            content.append(f'Creation date:     {created_at}\n')
            content.append(f'Last update:       {updated_at}\n')
            content.append(f'Sales contact ID:  {str(sales_contact.id)}\n')
            content.append(f'Sales contact:     {sales_contact.first_name.title()} {sales_contact.last_name.title()}')

            panel = Panel(
                content,
                title=f'Client #{result.id}',
            )

            console.print(panel)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@clients.command('update')
@click.option('--id', 'client_id', type=int, required=True)
@click.option('--last-name', type=str, required=False)
@click.option('--first-name', type=str, required=False)
@click.option('--email', type=str, required=False)
@click.option('--phone-number', type=str, required=False)
@click.option('--company-name', type=str, required=False)
def update_client(client_id, last_name, first_name, email, phone_number, company_name):
    '''Update a client by id.'''
    session = Session()

    try:
        client_repository = ClientRepository(session)
        client_controller = ClientController(client_repository)

        result = client_controller.update_client(
            client_id=client_id,
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name
        )

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        if result == 'user_not_sales_role':
            click.secho('Action restricted to the sales team.', fg='red')
            return
        
        if result == 'client_not_found':
            click.secho('Client was not found.', fg='red')
            return
        
        if result == 'user_not_client_contact':
            click.secho('You are not the contact of this client.', fg='red')
            return
        
        else:
            click.secho('Client successfully updated.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
