from exceptions import InsufficientFundsError, OverdraftLimitError


class BankAccount:
    """
    Base class representing a generic bank account.

    Attributes (private):
        __owner (str)        : The account holder's name.
        __balance (float)    : The current account balance.
        __transactions (list): Log of all deposits and withdrawals.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0):
        """
        Initialise a BankAccount.

        Args:
            owner (str)           : Name of the account holder.
            initial_balance (float): Opening balance. Defaults to 0.0.
        """
        self.__owner = owner
        self.__balance = 0.0
        self.__transactions = []

        if initial_balance > 0:
            self.__balance = float(initial_balance)
            self.__transactions.append(
                ("Opening deposit", initial_balance, self.__balance)
            )

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def deposit(self, amount: float, description: str = "Deposit") -> None:
        """
        Deposit a positive amount into the account.

        Args:
            amount (float)     : Amount to deposit (must be > 0).
            description (str)  : Label shown on the statement. Defaults to 'Deposit'.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += float(amount)
        self.__transactions.append((description, amount, self.__balance))

    def withdraw(self, amount: float) -> None:
        """
        Deduct a positive amount from the account balance.

        Subclasses override this to enforce extra rules, then call
        super().withdraw(amount) to complete the deduction.

        Args:
            amount (float): Amount to withdraw (must be > 0).

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        self.__balance -= float(amount)
        self.__transactions.append(("Withdrawal", -amount, self.__balance))

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self.__balance

    def get_statement(self) -> None:
        """Print all transactions with a running balance."""
        print(f"\n--- Statement for {self.__owner} ---")
        for description, amount, balance in self.__transactions:
            prefix = "+" if amount >= 0 else ""
            print(f"  {description}: {prefix}{amount:.1f} \u2502 Bal: {balance:.1f}")
        print(f"--- Current Balance: Rs.{self.__balance:.1f} ---\n")

    def transfer(self, amount: float, target_account: "BankAccount") -> None:
        """
        Transfer an amount from this account to another account.

        Calls self.withdraw() (which respects each subclass's rules),
        then deposits the same amount into target_account.

        Args:
            amount (float)               : Amount to transfer.
            target_account (BankAccount) : Destination account.

        Raises:
            InsufficientFundsError: If self is a SavingsAccount and the
                transfer would violate the minimum-balance rule.
            OverdraftLimitError: If self is a CurrentAccount and the
                transfer would exceed the overdraft limit.
        """
        self.withdraw(amount)
        target_account.deposit(amount, description="Transfer in")

    # ------------------------------------------------------------------
    # Property
    # ------------------------------------------------------------------

    @property
    def owner(self) -> str:
        """Return the account holder's name (read-only)."""
        return self.__owner


# ======================================================================


class SavingsAccount(BankAccount):
    """
    A savings account that enforces a minimum balance of Rs. 500.

    Attributes:
        interest_rate (float): Annual interest rate (e.g., 0.05 = 5 %).
        MIN_BALANCE (float)  : Class-level constant – Rs. 500.
    """

    MIN_BALANCE: float = 500.0

    def __init__(self, owner: str, initial_balance: float, interest_rate: float):
        """
        Initialise a SavingsAccount.

        Args:
            owner (str)            : Account holder's name.
            initial_balance (float): Opening balance.
            interest_rate (float)  : Annual interest rate, e.g. 0.05 for 5 %.
        """
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount: float) -> None:
        """
        Withdraw amount while keeping balance at or above Rs. 500.

        Args:
            amount (float): Amount to withdraw.

        Raises:
            InsufficientFundsError: If balance after withdrawal would fall
                below the minimum balance of Rs. 500.
        """
        if self.get_balance() - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                "Cannot withdraw. Min balance of Rs.500 must be maintained."
            )
        super().withdraw(amount)

    def add_interest(self) -> None:
        """
        Credit interest to the account.

        Calculates interest_rate × current balance and deposits it,
        logging the transaction as 'Interest credit'.
        """
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest, description="Interest credit")


# ======================================================================


class CurrentAccount(BankAccount):
    """
    A current account that permits a negative balance up to an overdraft limit.

    Attributes:
        overdraft_limit (float): Maximum negative balance allowed
            (e.g., 2000 means balance may fall as low as -2000).
    """

    def __init__(self, owner: str, initial_balance: float, overdraft_limit: float):
        """
        Initialise a CurrentAccount.

        Args:
            owner (str)             : Account holder's name.
            initial_balance (float) : Opening balance.
            overdraft_limit (float) : Overdraft ceiling (positive value).
        """
        super().__init__(owner, initial_balance)
        self.overdraft_limit = float(overdraft_limit)

    def withdraw(self, amount: float) -> None:
        """
        Withdraw amount, allowing balance to go negative within overdraft limit.

        Args:
            amount (float): Amount to withdraw.

        Raises:
            OverdraftLimitError: If the withdrawal would push the balance
                below -overdraft_limit.
        """
        if self.get_balance() - amount < -self.overdraft_limit:
            raise OverdraftLimitError(
                f"Overdraft limit of Rs.{int(self.overdraft_limit)} exceeded."
            )
        super().withdraw(amount)

