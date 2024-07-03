from sqlalchemy.exc import DatabaseError, IntegrityError
from pydantic import ValidationError
from datetime import datetime

from bank.infra.abstraction.transaction_repository import AbstractTransactionRepository
from bank.domain.models import Transaction
from bank.models import TransactionEntity
from bank.database import SessionManager
from bank import logger
from bank.infra.exceptions import DatabaseException, CustomerAlreadyExists


class TransactionRepository(AbstractTransactionRepository):

    def find_transactions_by_account_id(self, account_id) -> list[Transaction]:
        
        try:
            with SessionManager() as session:   

                if transactions := session.query(TransactionEntity).filter(
                    TransactionEntity.account_id==account_id).all():

                    return [Transaction(
                        transaction_id=transaction.transaction_id,
                        account_id=transaction.account_id,
                        transaction_type=transaction.transaction_type,
                        amount=transaction.amount,
                        date_of_transaction=transaction.date_of_transaction
                    ) for transaction in transactions]
                
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)


    def add_transaction(self, account_id, transaction_type, amount) -> Transaction:

        try:
            with SessionManager() as session:   
                transaction = Transaction(
                    transaction_id=None,
                    account_id=account_id,
                    transaction_type=transaction_type,
                    amount=amount,
                    date_of_transaction=datetime.now()
                )
                
                new_transaction = TransactionEntity(
                    account_id=account_id,
                    transaction_type=transaction_type,
                    amount=amount,
                )

                session.add(new_transaction)
                session.commit()

                transaction.transaction_id = new_transaction.transaction_id
                transaction.date_of_transaction = new_transaction.date_of_transaction

                return transaction

        except ValidationError as e:
            logger.exception("Invalid Value/s: %s", e)
            raise ValueError(e)
        
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)

