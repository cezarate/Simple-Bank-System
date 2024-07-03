from bank import models
from bank.database import engine
from bank.infra.account_repository import AccountRepository
from bank.infra.customer_repository import CustomerRepository
from bank.infra.transaction_repository import TransactionRepository
from bank.usecase.use_case import UseCase

models.Base.metadata.create_all(bind=engine)

# simple test scenario
uc = UseCase(account_repo=AccountRepository(),
             customer_repo=CustomerRepository(),
             transaction_repo=TransactionRepository())

account = uc.create_account("jadc", "Juana Dela Cruz", "juanadelacruz@abc.def", "12345543210")
uc.make_transaction(account_id=account.account_id, amount=10000, transaction_type="deposit")
uc.make_transaction(account_id=account.account_id, amount=5000, transaction_type="withdraw")
print(uc.generate_account_statements(account_id=account.account_id))
