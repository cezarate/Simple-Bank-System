""" This is the models file

It contains the models for the database tables for this API.
"""
from sqlalchemy import Column, String, Integer, UUID, Float, DateTime, ForeignKey
from datetime import datetime
import uuid
from typing_extensions import Optional
from bank.database import Base


class CustomerEntity(Base):
    __tablename__ = "customers"
    customer_id: Optional[String] = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)


class AccountEntity(Base):

    __tablename__ = "accounts"
    account_id: Optional[Integer] = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    account_number: Optional[UUID] = Column(UUID, unique=True, default=uuid.uuid4)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    balance = Column(Float)


class TransactionEntity(Base):

    __tablename__ = "transactions"

    transaction_id: Optional[Integer] = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    transaction_type = Column(String)
    amount = Column(Float)
    date_of_transaction = Column(DateTime, default=datetime.now())
