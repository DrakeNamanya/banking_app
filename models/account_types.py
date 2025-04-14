# models/account_types.py
from abc import ABC, abstractmethod
from datetime import datetime

class BankAccount(ABC):
    def __init__(self, account_number, balance=0):
        self._account_number = account_number
        self._balance = balance
        self._transactions = []

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @property
    def transactions(self):
        return self._transactions

    @property
    def account_type(self):
        return self.__class__.__name__.lower()

    def add_transaction(self, amount, transaction_type, note=""):
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "type": transaction_type,
            "note": note,
            "balance": self._balance
        }
        self._transactions.append(transaction)
        return transaction

class SavingAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.03):
        super().__init__(account_number, balance)
        self._interest_rate = interest_rate

    def deposit(self, amount, note=""):
        if amount > 0:
            self._balance += amount
            self.add_transaction(amount, "deposit", note)
            return True, f"Deposited UGX {amount}. New balance: UGX {self._balance}"
        return False, "Invalid deposit amount"

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.add_transaction(amount, "withdrawal")
            return True, f"Withdrew UGX {amount}. New balance: UGX {self._balance}"
        return False, "Insufficient funds"

class checkingAccount(BankAccount):
    def __init__(self, account_number, balance=0, empowerment_bonus=0.02):
        super().__init__(account_number, balance)
        self._empowerment_bonus = empowerment_bonus

    def deposit(self, amount, note=""):
        if amount > 0:
            bonus = amount * self._empowerment_bonus
            total = amount + bonus
            self._balance += total
            self.add_transaction(total, "deposit", f"{note} (+UGX {bonus} bonus)")
            return True, f"Deposited UGX {amount} (+UGX {bonus} bonus). New balance: UGX {self._balance}"
        return False, "Invalid deposit amount"

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.add_transaction(amount, "withdrawal")
            return True, f"Withdrew UGX {amount}. New balance: UGX {self._balance}"
        return False, "Insufficient funds"
