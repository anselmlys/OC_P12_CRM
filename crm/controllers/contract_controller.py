import sentry_sdk

from crm.services.auth_service import get_current_user_payload
from crm.services.authorization_service import is_authenticated, has_role
from crm.services.data_validation_service import (clean_optional_integer,
                                                  clean_required_integer,
                                                  clean_optional_boolean)


class ContractController:
    '''Handle contract-related operations with authentication and authorization checks.'''

    def __init__(self, contract_repository):
        self.contract_repository = contract_repository

    def get_all_contracts(self):
        '''Return a list of all contracts. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        contracts = self.contract_repository.get_all()
        return contracts

    def get_contract(self, contract_id):
        '''Return a contract. User must be authenticated.'''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        contract = self.contract_repository.get_by_id(contract_id)
        return contract

    def create_contract(self, client_id, total_amount=None,
                        remaining_amount=None, signed=False):
        '''
        Return new contract data after saving in database.
        User must be authenticated and have the role "management".
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'management'):
            return 'user_not_management_role'

        client_id = clean_required_integer(client_id, 'client_id')
        total_amount = clean_optional_integer(total_amount, 'total_amount')
        remaining_amount = clean_optional_integer(remaining_amount, 'remaining_amount')
        signed = clean_optional_boolean(signed, 'signed')

        contract = self.contract_repository.create_contract(
            client_id=client_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=signed,
        )

        return contract

    def get_unsigned_contracts(self):
        '''
        Return a list of all unsigned contracts.
        User must be authenticated and have the role "sales".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'sales'):
            return 'user_not_sales_role'

        contracts = self.contract_repository.get_unsigned_contracts()
        return contracts

    def get_unpaid_contracts(self):
        '''
        Return a list of all unpaid contracts.
        User must be authenticated and have the role "sales".
        '''
        payload = get_current_user_payload()
        if not is_authenticated(payload):
            return 'user_not_authenticated'

        if not has_role(payload, 'sales'):
            return 'user_not_sales_role'

        contracts = self.contract_repository.get_contracts_with_remaining_amounts()
        return contracts

    def update_contract(self, contract_id, client_id=None, total_amount=None,
                        remaining_amount=None, signed=None):
        '''
        Return updated contract after saving in database.
        User must be authenticated and have the role "management"
        or be the client's sales contact.
        '''
        payload = get_current_user_payload()

        if not is_authenticated(payload):
            return 'user_not_authenticated'

        contract = self.contract_repository.get_by_id(contract_id)
        if contract is None:
            return 'contract_not_found'

        was_signed = contract.signed is True

        if (
            not has_role(payload, 'management')
            and payload['sub'] != str(contract.client.sales_contact_id)
        ):
            return 'user_not_client_contact'

        updates = {}

        if client_id is not None:
            updates['client_id'] = clean_optional_integer(client_id, 'client_id')

        if total_amount is not None:
            updates['total_amount'] = clean_optional_integer(total_amount, 'total_amount')

        if remaining_amount is not None:
            updates['remaining_amount'] = clean_optional_integer(
                remaining_amount, 'remaining_amount')

        if signed is not None:
            updates['signed'] = clean_optional_boolean(signed, 'signed')

        updated_contract = self.contract_repository.update_object(contract.id, updates)

        # Send message to sentry if the contract get signed
        if not was_signed and updated_contract.signed is True:
            sentry_sdk.capture_message(
                    f'Contract signed: {contract_id}',
                    level='info',
                )

        return updated_contract
