from sqlalchemy.exc import DatabaseError, IntegrityError
from pydantic import ValidationError

from bank.infra.abstraction.customer_repository import AbstractCustomerRepository
from bank.domain.models import Customer
from bank.models import CustomerEntity
from bank.database import SessionManager
from bank import logger
from bank.infra.exceptions import DatabaseException, CustomerAlreadyExists

class CustomerRepository(AbstractCustomerRepository):


    def add_customer(self, customer_id, name, email, phone_number) -> Customer:

        try:
            with SessionManager() as session:

                # Validate customer data
                customer = Customer(
                    customer_id=customer_id,
                    name=name,
                    email=email,
                    phone_number=phone_number
                )        

                customer_to_add = CustomerEntity(
                    customer_id=customer_id,
                    name=name,
                    email=email,
                    phone_number=phone_number
                )

                if existing_customer := session.query(CustomerEntity).filter(
                    CustomerEntity.customer_id==customer.customer_id).one_or_none():

                    if existing_customer.name == customer_to_add.name and \
                        existing_customer.email == customer_to_add.email and \
                        existing_customer.phone_number == customer_to_add.phone_number:
                        return customer

                session.add(customer_to_add)
                session.commit()

                return customer_to_add

        except ValidationError as e:
            logger.exception("Invalid Value/s: %s", e)
            raise ValueError(e)
        
        except IntegrityError as e:
            logger.exception("A record already exists with one or more same fields: %s", e)
            raise CustomerAlreadyExists(e)
        
        except DatabaseError as e:
            logger.exception("Database Error: %s", e)
            raise DatabaseException(e)

