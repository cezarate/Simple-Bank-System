from abc import abstractmethod, ABC
from bank.domain.models import Account

class AbstractAccountRepository(ABC):

    @abstractmethod
    def add_account(self, customer_id) -> Account:
        pass

    @abstractmethod
    def save_account(self, account: Account) -> bool:
        pass

    @abstractmethod
    def find_account_by_id(self, account_id) -> Account | None:
        pass

    @abstractmethod
    def find_accounts_by_customer_id(self, customer_id) -> list[Account]:
        pass
