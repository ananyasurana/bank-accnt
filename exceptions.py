class InsufficientFundsError(Exception):
    """Raised when a SavingsAccount withdrawal would violate the Rs.500 minimum balance."""
    pass


class OverdraftLimitError(Exception):
    """Raised when a CurrentAccount withdrawal would exceed the overdraft limit."""
    pass

