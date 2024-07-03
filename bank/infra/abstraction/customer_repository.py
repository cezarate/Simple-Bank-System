from abc import abstractmethod, ABC
from bank.domain.models import Customer
class AbstractCustomerRepository(ABC):

    @abstractmethod
    def add_customer(self, customer_id, name, email, phone_number) -> Customer:
        pass
