from bank_account import SavingsAccount, CurrentAccount
from exceptions import InsufficientFundsError, OverdraftLimitError

DIVIDER = "=" * 55


def test_case_1():
    """Savings — minimum balance enforcement."""
    print(DIVIDER)
    print("TEST CASE 1 — Savings: Minimum Balance Enforcement")
    print(DIVIDER)

    acc = SavingsAccount("Alice", 1000, 0.05)
    acc.deposit(500)        # balance → 1500
    acc.withdraw(900)       # balance → 600  (valid)
    print(f"Balance after valid withdrawal: Rs.{acc.get_balance()}")  # 600.0

    try:
        acc.withdraw(200)   # balance would be 400 < 500  (invalid)
    except InsufficientFundsError as e:
        print(f"InsufficientFundsError: {e}")


def test_case_2():
    """Current — overdraft limit enforcement."""
    print(DIVIDER)
    print("TEST CASE 2 — Current: Overdraft Limit Enforcement")
    print(DIVIDER)

    acc = CurrentAccount("Bob", 500, 2000)
    acc.withdraw(2000)      # balance → -1500  (valid)
    print(f"Balance after valid withdrawal: Rs.{acc.get_balance()}")  # -1500.0

    try:
        acc.withdraw(600)   # balance would be -2100 (invalid)
    except OverdraftLimitError as e:
        print(f"OverdraftLimitError: {e}")


def test_case_3():
    """Interest calculation & statement."""
    print(DIVIDER)
    print("TEST CASE 3 — Interest Calculation & Statement")
    print(DIVIDER)

    acc = SavingsAccount("Carol", 2000, 0.05)
    acc.add_interest()      # 5 % of 2000 = 100  →  balance 2100
    print(f"Balance after interest: Rs.{acc.get_balance()}")  # 2100.0
    acc.get_statement()


def test_bonus_transfer():
    """Bonus — transfer between account types."""
    print(DIVIDER)
    print("BONUS — Transfer Between Account Types")
    print(DIVIDER)

    savings = SavingsAccount("Dave", 2000, 0.05)
    current = CurrentAccount("Eve", 300, 1000)

    print(f"Dave (Savings) before transfer: Rs.{savings.get_balance()}")
    print(f"Eve  (Current) before transfer: Rs.{current.get_balance()}")

    savings.transfer(1000, current)   # Dave: 2000 → 1000, Eve: 300 → 1300

    print(f"Dave (Savings) after  transfer: Rs.{savings.get_balance()}")
    print(f"Eve  (Current) after  transfer: Rs.{current.get_balance()}")
    current.get_statement()


if __name__ == "__main__":
    test_case_1()
    print()
    test_case_2()
    print()
    test_case_3()
    print()
    test_bonus_transfer()


