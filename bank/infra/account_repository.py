from sqlalchemy.exc import DatabaseError, MultipleResultsFound
from pydantic import ValidationError

from bank.infra.abstraction.account_repository import AbstractAccountRepository
from bank.domain.models import Account
from bank.models import AccountEntity
from bank.database import SessionManager
from bank import logger
from bank.infra.exceptions import DuplicateAccountsFound, DatabaseException


class AccountRepository(AbstractAccountRepository):

    def add_account(self, customer_id) -> Account:
        try:
            with SessionManager() as session:   
                account = Account(
                    account_id=None,
                    account_number=None,
                    customer_id=customer_id,
                    balance=0
                )
                
                new_account = AccountEntity(
                    customer_id=customer_id,
                    balance=0
                )

                session.add(new_account)
                session.commit()

                account.account_id = new_account.account_id
                account.account_number = new_account.account_number

                return account

        except ValidationError as e:
            logger.exception("Invalid Value/s: %s", e)
            raise ValueError(e)
        
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)

    def save_account(self, account: Account) -> bool:

        try:
            with SessionManager() as session:   

                if existing_account := session.query(AccountEntity).filter(
                    AccountEntity.account_id==account.account_id).one_or_none():

                    existing_account.balance = account.balance

                    session.add(existing_account)
                    session.commit()

                return True

        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)
        

    def find_account_by_id(self, account_id) -> Account | None:

        try:
            with SessionManager() as session:   

                if account := session.query(AccountEntity).filter(
                    AccountEntity.account_id==account_id).one_or_none():

                    return Account(
                        account_id=account.account_id,
                        account_number=account.account_number,
                        customer_id=account.customer_id,
                        balance=account.balance
                    )
                
                return None
                
        except MultipleResultsFound as e:
            logger.exception("Multiple accounts found with the same id: %s", e)
            raise DuplicateAccountsFound(e)
        
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)

    def find_accounts_by_customer_id(self, customer_id) -> list[Account]:

        try:
            with SessionManager() as session:   

                if accounts := session.query(AccountEntity).filter(
                    AccountEntity.customer_id==customer_id).all():

                    return [Account(
                        account_id=account.account_id,
                        account_number=account.account_number,
                        customer_id=account.customer_id,
                        balance=account.balance
                    ) for account in accounts]
                
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)


