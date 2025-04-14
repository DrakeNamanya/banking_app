from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_number, balance=0):
        self._account_number = account_number
        self._balance = balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self._balance = amount
        else:
            raise ValueError("Balance cannot be negative")

    @abstractmethod
    def deposit(self, amount, note=None):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.05):
        super().__init__(account_number, balance)
        self._interest_rate = interest_rate

    def deposit(self, amount, note=None):
        if amount > 0:
            self.balance += amount
            return True, f"Deposited {amount} to savings account {self.account_number}. New balance: {self.balance}"
        return False, "Invalid deposit amount"

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True, f"Withdrew {amount} from savings account {self.account_number}. New balance: {self.balance}"
        return False, "Invalid withdrawal amount or insufficient balance"

    def calculate_interest(self):
        interest = self.balance * self._interest_rate
        success, message = self.deposit(interest)
        return success, f"Interest of {interest} added. {message}"

class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance=0, overdraft_limit=500):
        super().__init__(account_number, balance)
        self._overdraft_limit = overdraft_limit

    def deposit(self, amount, note=None):
        if amount > 0:
            self.balance += amount
            return True, f"Deposited {amount} to checking account {self.account_number}. New balance: {self.balance}"
        return False, "Invalid deposit amount"

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self._overdraft_limit:
            self.balance -= amount
            return True, f"Withdrew {amount} from checking account {self.account_number}. New balance: {self.balance}"
        return False, "Withdrawal amount exceeds overdraft limit"

# In-memory storage for accounts
accounts = {}