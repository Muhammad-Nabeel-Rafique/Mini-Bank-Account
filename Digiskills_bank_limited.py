import os
import re
from datetime import datetime


class Customer:
    """Class to store customer details."""

    def __init__(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id


class Account:
    """Class to manage password-protected account operations for Digiskills Bank Limited."""

    BANK_NAME = "Digiskills Bank Limited"

    def __init__(self, account_number, customer, password, balance=0.0):
        self.account_number = account_number
        self.customer = customer
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        """Deposits money into the account and generates a receipt."""
        try:
            if amount <= 0:
                print("\n Error: Deposit amount must be greater than zero.")
                return
            self.balance += amount
            print(
                f"\n Successfully deposited ${amount:.2f}. New Balance: ${self.balance:.2f}"
            )
            self._generate_receipt("DEPOSIT / CREDIT", amount)
        except Exception as e:
            print(f"\n An unexpected error occurred during deposit: {e}")

    def withdraw(self, amount):
        """Withdraws money from the account and generates a receipt."""
        try:
            if amount <= 0:
                print("\n Error: Withdrawal amount must be greater than zero.")
            elif amount > self.balance:
                print(
                    f"\n Error: Insufficient funds! Current balance is ${self.balance:.2f}."
                )
            else:
                self.balance -= amount
                print(
                    f"\n Successfully withdrew ${amount:.2f}. Remaining Balance: ${self.balance:.2f}"
                )
                self._generate_receipt("WITHDRAWAL / DEBIT", amount)
        except Exception as e:
            print(f"\n An unexpected error occurred during withdrawal: {e}")

    def display_balance(self):
        """Displays account summary."""
        print(f"\n========================================")
        print(f"         {self.BANK_NAME}")
        print(f"          ACCOUNT STATEMENT")
        print(f"========================================")
        print(f"Account Holder: {self.customer.name}")
        print(f"Customer ID:    {self.customer.customer_id}")
        print(f"Account No:     {self.account_number}")
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"========================================\n")

    def _generate_receipt(self, transaction_type, amount):
        """Generates and saves a transaction receipt with file system error handling."""
        folder_name = "receipts"
        try:
            os.makedirs(folder_name, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{folder_name}/receipt_{self.account_number}_{timestamp}.txt"

            receipt_content = f"""========================================
         {self.BANK_NAME}
           TRANSACTION RECEIPT
========================================
Date/Time:       {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Customer Name:   {self.customer.name}
Customer ID:     {self.customer.customer_id}
Account Number:  {self.account_number}
----------------------------------------
Transaction:     {transaction_type}
Amount:          ${amount:.2f}
Updated Balance: ${self.balance:.2f}
========================================
     Thank you for banking with us!
========================================
"""
            with open(filename, "w", encoding="utf-8") as file:
                file.write(receipt_content)

            print(f" Receipt saved to: {filename}\n")

        except PermissionError:
            print(
                f"\n File Error: Permission denied while writing to '{folder_name}' folder."
            )
        except OSError as e:
            print(f"\n File Error: Failed to save receipt file: {e}")


def check_password_strength(password):
    """
    Validates password strength.
    Requires: >= 8 characters, at least 1 uppercase letter, 1 lowercase letter, 1 digit, 1 special character.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter (A-Z)."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter (a-z)."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit (0-9)."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    return True, "Strong Password"


def get_positive_float(prompt):
    """Helper function to safely handle numeric user inputs."""
    while True:
        user_input = input(prompt).strip()
        try:
            value = float(user_input)
            if value < 0:
                print(" Error: Amount cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print(
                " Error: Invalid entry! Please enter a valid numerical value."
            )


def get_secure_password():
    """Prompts user for password until a strong password is provided."""
    while True:
        password = input("Create a Password: ").strip()
        is_strong, msg = check_password_strength(password)
        if is_strong:
            print(" Password strength validated (STRONG).")
            return password
        else:
            print(f" Error: Weak Password — {msg}")


def logged_in_menu(account):
    """Sub-menu accessible only after successful authentication."""
    while True:
        print(f"\n--- WELCOME, {account.customer.name.upper()} ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Logout")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            amount = get_positive_float("Enter deposit amount ($): ")
            account.deposit(amount)

        elif choice == "2":
            amount = get_positive_float("Enter withdrawal amount ($): ")
            account.withdraw(amount)

        elif choice == "3":
            account.display_balance()

        elif choice == "4":
            print(f"\nLogged out successfully from account {account.account_number}.")
            break
        else:
            print(" Error: Invalid option! Select 1 to 4.")


def main():
    """Main system menu for Digiskills Bank Limited."""
    accounts = {}
    acc_counter = 1001

    while True:
        print("\n=== DIGISKILLS BANK LIMITED ===")
        print("1. Create New Account")
        print("2. Login to Account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            name = input("Enter customer name: ").strip()
            if not name:
                print(" Error: Customer name cannot be empty.")
                continue

            cust_id = f"CUST{acc_counter}"
            acc_num = f"ACC{acc_counter}"

            password = get_secure_password()
            initial_deposit = get_positive_float(
                "Enter initial deposit amount ($): "
            )

            customer = Customer(name, cust_id)
            account = Account(acc_num, customer, password, initial_deposit)
            accounts[acc_num] = account

            acc_counter += 1
            print(f"\n Account Created Successfully!")
            print(
                f"Assigned Account Number: {acc_num} | Customer ID: {cust_id}"
            )

        elif choice == "2":
            if not accounts:
                print(
                    "\n Error: Access Denied! No accounts exist in the system."
                )
                print("You must create an account first before logging in.")
                continue

            acc_num = input("Enter Account Number: ").strip().upper()

            if acc_num not in accounts:
                print(
                    f"\n Error: Login Failed! Account '{acc_num}' does not exist."
                )
                print("Please create an account first or check your Account Number.")
                continue

            password_attempt = input("Enter Password: ").strip()
            target_account = accounts[acc_num]

            if password_attempt == target_account.password:
                print("\n Login Successful!")
                logged_in_menu(target_account)
            else:
                print("\n Error: Authentication Failed! Incorrect password.")

        elif choice == "3":
            print(
                "\nThank you for choosing Digiskills Bank Limited. Goodbye! \nRegards, CEO: Muhammad Nabeel Rafique"
            )
            break

        else:
            print(" Error: Invalid choice! Please select 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

