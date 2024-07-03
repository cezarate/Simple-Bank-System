from bank import models
from bank.database import engine
from bank.infra.account_repository import AccountRepository
from bank.infra.customer_repository import CustomerRepository
from bank.infra.transaction_repository import TransactionRepository
from bank.models import AccountEntity, CustomerEntity, TransactionEntity
from bank.usecase.use_case import UseCase
from bank.database import SessionManager


def test_simple_scenario():
    models.Base.metadata.create_all(bind=engine)

    # simple test scenario
    uc = UseCase(account_repo=AccountRepository(),
                customer_repo=CustomerRepository(),
                transaction_repo=TransactionRepository())

    account = uc.create_account("jadc", "Juana Dela Cruz", "juanadelacruz@abc.def", "12345543210")
    uc.make_transaction(account_id=account.account_id, amount=10000, transaction_type="deposit")
    uc.make_transaction(account_id=account.account_id, amount=5000, transaction_type="withdraw")
    uc.generate_account_statements(account_id=account.account_id)

    with SessionManager() as session:
        assert session.query(CustomerEntity).filter(
            CustomerEntity.customer_id=="jadc",
            CustomerEntity.name=="Juana Dela Cruz",
            CustomerEntity.email=="juanadelacruz@abc.def",
            CustomerEntity.phone_number=="12345543210",
        ).one_or_none()
        assert session.query(AccountEntity).filter(
            AccountEntity.account_id==account.account_id,
            AccountEntity.balance==5000
        ).one_or_none()
        assert session.query(TransactionEntity).filter(
            TransactionEntity.account_id==account.account_id,
            TransactionEntity.transaction_type=='deposit',
            TransactionEntity.amount==10000
        ).one_or_none()
        assert session.query(TransactionEntity).filter(
            TransactionEntity.account_id==account.account_id,
            TransactionEntity.transaction_type=='withdraw',
            TransactionEntity.amount==5000
        ).one_or_none()

    
