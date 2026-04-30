import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from crm.db import Session
from crm.repositories.contract_repository import ContractRepository
from crm.controllers.contract_controller import ContractController


@click.group()
def contracts():
    '''Manage contracts.'''
    pass


@contracts.command('create')
@click.option('--client-id', type=int, required=True)
@click.option('--total-amount', type=int, required=False)
@click.option('--remaining-amount', type=int, required=False)
@click.option('--signed', help='Format: (yes/no)', type=str, default='no')
def create_contract(client_id, total_amount, remaining_amount, signed):
    '''Create a new contract.'''
    session = Session()

    try:
        contract_repository = ContractRepository(session)
        contract_controller = ContractController(contract_repository)

        result = contract_controller.create_contract(client_id, total_amount, remaining_amount, signed)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        if result == 'user_not_management_role':
            click.secho('Action restricted to the management team.', fg='red')
            return
        
        else:
            click.secho('Contract successfully created.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@contracts.command('list')
@click.option('--unsigned', is_flag=True, help='Show only unsigned contracts.')
@click.option('--unpaid', is_flag=True, help='Show only unpaid contracts.')
def get_contracts(unsigned, unpaid):
    '''List all contracts.'''
    session = Session()

    try:
        contract_repository = ContractRepository(session)
        contract_controller = ContractController(contract_repository)

        if unsigned:
            result = contract_controller.get_unsigned_contracts()
        elif unpaid:
            result = contract_controller.get_unpaid_contracts()
        else:
            result = contract_controller.get_all_contracts()

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        if result == 'user_not_sales_role':
            click.secho('Action restricted to the sales team.', fg='red')
            return
        
        else:
            console = Console()

            table = Table(title='Contracts', show_lines=True)

            table.add_column('ID', justify='right', no_wrap=True)
            table.add_column('Client ID', justify='left', no_wrap=True)
            table.add_column('Client', justify='left', no_wrap=True)
            table.add_column('Event ID', justify='left', no_wrap=True)

            for contract in result:
                event = contract.event or '-'

                table.add_row(
                    str(contract.id),
                    str(contract.client.id),
                    f'{contract.client.first_name.title()} {contract.client.last_name.title()}',
                    str(event.id)
                )

            console.print(table)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@contracts.command('detail')
@click.option('--id', 'contract_id', type=int, required=True)
def get_contract(contract_id):
    '''Display a contract's details using its id.'''
    session = Session()

    try:
        contract_repository = ContractRepository(session)
        contract_controller = ContractController(contract_repository)

        result = contract_controller.get_contract(contract_id)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        else:
            console = Console()

            total_amount = result.total_amount or '-'
            remaining_amount = result.remaining_amount or '-'

            created_at = result.created_at.strftime('%d/%m/%Y %H:%M')
            if result.signed:
                signed = 'Yes'
            else:
                signed = 'No'

            content = Text()
            content.append(f'ID:                {str(result.id)}\n')
            content.append(f'Client ID:         {str(result.client.id)}\n')
            content.append(f'Client:            {result.client.first_name.title()} {result.client.last_name.title()}\n')
            content.append(f'Total amount:      {str(total_amount)}\n')
            content.append(f'Remaining amount:  {str(remaining_amount)}\n')
            content.append(f'Creation date:     {created_at}\n')
            content.append(f'Signed:            {signed}\n')
            content.append(f'Event ID:          {str(result.event.id)}\n')

            panel = Panel(
                content,
                title=f'Contract #{result.id}'
            )

            console.print(panel)

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()


@contracts.command('update')
@click.option('--id', 'contract_id', type=int, required=True)
@click.option('--client-id', type=int, required=False)
@click.option('--total-amount', type=int, required=False)
@click.option('--remaining-amount', type=int, required=False)
@click.option('--signed', help='Format: (yes/no)', type=str, required=False)
def update_contract(contract_id, client_id, total_amount, remaining_amount, signed):
    '''Update a contract by id.'''
    session = Session()

    try:
        contract_repository = ContractRepository(session)
        contract_controller = ContractController(contract_repository)

        result = contract_controller.update_contract(contract_id, client_id, total_amount, remaining_amount, signed)

        if result == 'user_not_authenticated':
            click.secho('Please login first.', fg='red')
            return
        
        if result == 'contract_not_found':
            click.secho('Contract not found.', fg='red')
            return
        
        if result == 'user_not_client_contact':
            click.secho('You are not the contact of this client.', fg='red')
            return
        
        else:
            click.secho('Contract successfully updated.', fg='green')

    except (ValueError, TypeError) as e:
        click.secho(f'Error: {e}', fg='red')

    except RuntimeError as e:
        click.secho(f'Error: {e}', fg='red')

    finally:
        session.close()
