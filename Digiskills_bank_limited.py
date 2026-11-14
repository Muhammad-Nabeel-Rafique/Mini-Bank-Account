import os
import re
from datetime import datetime


def _encrypt_security_image(image_data, password):
    """Encrypts an image using a key derived from the account password."""
    import base64

    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    salt = os.urandom(16)
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    ).derive(password.encode("utf-8"))
    token = Fernet(base64.urlsafe_b64encode(key)).encrypt(image_data)
    return salt + token


def _decrypt_security_image(encrypted_data, password):
    """Decrypts an image previously encrypted with the same account password."""
    import base64

    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    salt = encrypted_data[:16]
    if len(salt) != 16 or len(encrypted_data) <= 16:
        raise ValueError("Security image data is incomplete.")

    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    ).derive(password.encode("utf-8"))
    return Fernet(base64.urlsafe_b64encode(key)).decrypt(encrypted_data[16:])


def _save_security_image(account, image_data, storage_root="security_alerts"):
    """Saves an encrypted security image for an account."""
    account_folder = os.path.join(storage_root, account.account_number)
    os.makedirs(account_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"failed_login_{timestamp}.enc"
    filepath = os.path.join(account_folder, filename)

    with open(filepath, "xb") as file:
        file.write(_encrypt_security_image(image_data, account.password))
    return filepath


def capture_security_image(account):
    """Captures and encrypts one webcam image after a failed login."""
    try:
        import cv2
    except ImportError:
        print(
            "\n Security image unavailable: OpenCV is missing. "
            "Install dependencies with 'python -m pip install -r requirements.txt'."
        )
        return

    camera = None
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("\n Security image unavailable: no accessible camera was found.")
            return

        captured, frame = camera.read()
        if not captured:
            print("\n Security image unavailable: the camera could not capture an image.")
            return

        encoded, image_data = cv2.imencode(".png", frame)
        if not encoded:
            print("\n Security image unavailable: the captured image could not be encoded.")
            return

        filepath = _save_security_image(account, image_data.tobytes())
        print(f"\n Encrypted security image saved to: {filepath}")
    except ImportError:
        print(
            "\n Security image unavailable: the cryptography package is missing. "
            "Install dependencies with 'python -m pip install -r requirements.txt'."
        )
    except (OSError, cv2.error) as error:
        print(f"\n Security image could not be saved: {error}")
    finally:
        if camera is not None:
            camera.release()


def view_security_images(account):
    """Displays decrypted security images for an authenticated account."""
    try:
        import cv2
        import numpy as np
        from cryptography.fernet import InvalidToken
    except ImportError:
        print(
            "\n Security images unavailable: required packages are missing. "
            "Install dependencies with 'python -m pip install -r requirements.txt'."
        )
        return

    account_folder = os.path.join("security_alerts", account.account_number)
    try:
        filenames = sorted(
            filename
            for filename in os.listdir(account_folder)
            if filename.endswith(".enc")
        )
    except FileNotFoundError:
        filenames = []
    except OSError as error:
        print(f"\n Security images could not be opened: {error}")
        return

    if not filenames:
        print("\n No security images have been saved for this account.")
        return

    print("\n Security images are decrypted only for display. Press any key to continue.")
    try:
        for filename in filenames:
            filepath = os.path.join(account_folder, filename)
            try:
                with open(filepath, "rb") as file:
                    image_data = _decrypt_security_image(
                        file.read(), account.password
                    )
                image = cv2.imdecode(
                    np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR
                )
                if image is None:
                    print(f" Could not decode security image: {filename}")
                    continue
                cv2.imshow("Failed Login Security Image", image)
                if cv2.waitKey(0) == 27:
                    break
            except InvalidToken:
                print(f" Could not decrypt security image: {filename}")
            except (OSError, ValueError, cv2.error) as error:
                print(f" Could not display security image '{filename}': {error}")
    finally:
        try:
            cv2.destroyAllWindows()
        except cv2.error as error:
            print(f"\n Security image window could not be closed: {error}")


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
        print("5. View Security Images")

        choice = input("Enter your choice (1-5): ").strip()

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
        elif choice == "5":
            view_security_images(account)
        else:
            print(" Error: Invalid option! Select 1 to 5.")


def main():
    """Main system menu for Digiskills Bank Limited."""
    accounts = {}
    acc_counter = 1001

    print(
        "\nPrivacy notice: a failed password attempt will try to capture one image "
        "using the available webcam. Captures are encrypted with the account password "
        "and can be viewed after a successful login."
    )

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
                print("Attempting to capture an encrypted security image.")
                capture_security_image(target_account)

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

