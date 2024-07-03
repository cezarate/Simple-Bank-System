#pylint: disable=no-member
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing_extensions import Optional
from uuid import UUID


class Customer(BaseModel):

    customer_id: Optional[str]
    name: str
    email: EmailStr
    phone_number: str


class Account(BaseModel):

    account_id: Optional[int]
    account_number: Optional[UUID]
    customer_id: str
    balance: float

    def deposit(self, amount):
        if amount < 0:
            return False
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        return self.balance
        
    def get_balance(self):
        return self.balance


class Transaction(BaseModel):

    transaction_id: Optional[int]
    account_id: int
    transaction_type: str
    amount: float
    date_of_transaction: datetime
