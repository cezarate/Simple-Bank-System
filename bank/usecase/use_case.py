from bank import logger
from bank.infra.abstraction.account_repository import AbstractAccountRepository
from bank.infra.abstraction.customer_repository import AbstractCustomerRepository
from bank.infra.abstraction.transaction_repository import AbstractTransactionRepository
from bank.domain.models import Account

class UseCase:

    def __init__(self, account_repo: AbstractAccountRepository,
                 customer_repo: AbstractCustomerRepository,
                 transaction_repo: AbstractTransactionRepository):
        self.account_repository = account_repo
        self.customer_repository = customer_repo
        self.transaction_repository = transaction_repo

    def create_account(self, customer_id, name, email, phone_number) -> Account:
       
        customer = self.customer_repository.add_customer(
            customer_id=customer_id,
            name=name,
            email=email,
            phone_number=phone_number
        )

        if not customer:
            logger.error("An error has occurred in creating your profile.")
            return False
       
        account = self.account_repository.add_account(customer_id=customer_id)
       
        if not account:
            logger.error("An error has occurred in creating your account.")
            return False

        return account
   
    def make_transaction(self, account_id, amount, transaction_type) -> float:
        account = self.account_repository.find_account_by_id(account_id)

        if not account:
            logger.error("Account_id %s does not exist.", account_id)          
            return False
        
        match transaction_type:
            case 'deposit':
                balance = account.deposit(amount)
            case 'withdraw':
                balance = account.withdraw(amount)
            case _:
                logger.error("Invalid transaction type")
                return False
            
        if not balance:
            logger.error("%s transaction failed.", transaction_type)
            return False
        
        if not self.transaction_repository.add_transaction(
                account_id=account_id,
                transaction_type=transaction_type,
                amount=amount
            ):
            logger.error("An error occurred while processing your transaction.")
            return False
        
        self.account_repository.save_account(account=account)
            
        return balance

    def generate_account_statements(self, account_id) -> str:
        account_statement = ""
        account = self.account_repository.find_account_by_id(account_id=account_id)

        if not account:
            logger.error("Account_id %s does not exist.", account_id)
            return False
        
        transactions = self.transaction_repository.find_transactions_by_account_id(
            account_id=account_id)
            
        if len(transactions) == 0:
            return "No transactions found."
        
        for transaction in transactions:
            account_statement += f"timestamp: {transaction.date_of_transaction}\t transaction type: {transaction.transaction_type}\t amount: {transaction.amount}\n"
        return account_statement.strip()

