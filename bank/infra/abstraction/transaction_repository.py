from abc import abstractmethod, ABC
from bank.domain.models import Transaction

class AbstractTransactionRepository(ABC):

    @abstractmethod
    def find_transactions_by_account_id(self, account_id) -> list[Transaction]:
        pass
   
    @abstractmethod
    def add_transaction(self, account_id, transaction_type, amount) -> Transaction:
        pass