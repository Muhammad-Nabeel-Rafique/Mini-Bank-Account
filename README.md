# 🏦 Digiskills Bank Limited – CLI Banking System

<p align="center">
  <strong>💳 A Secure, Object-Oriented Banking Experience in Python</strong>
</p>

<p align="center">
  A command-line banking application featuring account management, secure authentication, deposits, withdrawals, automated transaction receipts, and encrypted security image capture.
</p>

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/Programming-Object--Oriented-purple)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv&logoColor=white)
![Cryptography](https://img.shields.io/badge/Security-Fernet%20Encryption-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub Stars](https://img.shields.io/github/stars/Muhammad-Nabeel-Rafique/Mini-Bank-Account?style=flat&logo=github)

---

## 🌟 About The Project

**Digiskills Bank Limited – CLI Banking System** is a Python-based banking application designed to simulate essential banking operations through an interactive command-line interface.

Built using Object-Oriented Programming (OOP), this project allows users to create accounts, authenticate themselves using passwords, deposit money, withdraw funds, and check their account balances.

But this banking system goes beyond basic banking operations!

It also incorporates additional security features, including strong password validation, encrypted security image capture after failed login attempts, and automatic transaction receipt generation.

The application combines Python programming concepts with practical file handling, encryption, and computer vision.

**Manage Your Money. Protect Your Account. Experience Smart Banking!** 🔐

---

## 🚀 Key Features

### 🏦 Banking Operations

- **Account Creation:** Creates customer accounts with automatically generated account numbers and customer IDs.
- **Secure Login:** Requires account number and password authentication.
- **Deposit Money:** Allows customers to deposit money into their accounts.
- **Withdraw Money:** Supports withdrawals with insufficient balance protection.
- **Balance Inquiry:** Displays customer information and current account balance.
- **Account Management:** Provides a dedicated menu for authenticated customers.
- **Logout:** Allows customers to safely exit their account session.

### 🔐 Security Features

- **Strong Password Validation:** Requires at least 8 characters, including uppercase letters, lowercase letters, digits, and special characters.
- **Password Authentication:** Verifies passwords before granting account access.
- **Failed Login Security Capture:** Attempts to capture a webcam image after an incorrect password for an existing account.
- **Image Encryption:** Encrypts captured security images using Fernet encryption.
- **Password-Based Key Derivation:** Uses PBKDF2-HMAC with SHA-256 and 600,000 iterations to derive encryption keys.
- **Random Salt:** Generates a unique 16-byte salt for each encrypted image.
- **Protected Image Viewing:** Allows authenticated customers to view their decrypted security images.

### 🧾 Transaction Management

- **Automatic Receipt Generation:** Creates a text receipt after every successful deposit or withdrawal.
- **Timestamped Receipts:** Includes transaction date and time.
- **Transaction Details:** Records customer information, account number, transaction type, amount, and updated balance.
- **Automatic File Storage:** Saves receipts inside a dedicated `receipts/` directory.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OOP | Customer and account management |
| OpenCV | Webcam access and image capture |
| Cryptography | Fernet encryption and secure key derivation |
| NumPy | Image decoding for security image viewing |
| Regular Expressions | Password strength validation |
| File Handling | Saving transaction receipts and encrypted images |
| Unittest | Automated security testing |

---

## 📂 Project Structure

```text
Mini-Bank-Account/
│
├── security_alerts/          # Encrypted security images
│   └── ACC1001/
│       └── failed_login_*.enc
│
├── receipts/                 # Generated transaction receipts
│   └── receipt_*.txt
│
├── .gitignore                # Git ignore configuration
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── requirements.txt          # Required dependencies
│
├── Digiskills_bank_limited.py  # Main banking application
└── test_security_alerts.py     # Automated security tests
```
Note: The "receipts/" and "security_alerts/" directories are created automatically when the application generates its first receipt or saves its first security image.

---

⚙️ Installation & Setup

Follow these steps to install and run the application.

1. Clone the Repository
```
git clone https://github.com/Muhammad-Nabeel-Rafique/Mini-Bank-Account.git
```
2. Navigate to the Project Directory
```
cd Mini-Bank-Account
```
3. Create a Virtual Environment
```
python -m venv .venv
```
4. Install Dependencies

Windows (Command Prompt / PowerShell):
```
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
Linux / macOS:
```
source .venv/bin/activate
pip install -r requirements.txt
```
The project uses the following external Python packages:

- "cryptography"
- "opencv-python"
- "numpy"

The remaining modules are included in Python's standard library.

---

▶️ Running the Application

After installing the dependencies, start the banking application.

Windows:
```
.\.venv\Scripts\python.exe Digiskills_bank_limited.py
```
Linux / macOS:
```
python Digiskills_bank_limited.py
```
---

🎮 How to Use

Once the application starts, the main menu will appear:

=== DIGISKILLS BANK LIMITED ===

1. Create New Account
2. Login to Account
3. Exit

Enter your choice (1-3):

📝 Creating a New Account

1. Select option "1".
2. Enter your customer name.
3. Create a strong password.
4. Enter your initial deposit amount.
5. Your account number and customer ID will be generated automatically.

Example:

Assigned Account Number: ACC1001
Customer ID: CUST1001

🔑 Logging Into Your Account

1. Select option "2".
2. Enter your account number.
3. Enter your password.
4. After successful authentication, the customer menu will appear.

💳 Customer Menu

--- WELCOME, CUSTOMER ---

1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Logout
5. View Security Images

Enter your choice (1-5):

Choose the operation you want to perform.

---

🔐 Security System Explained

One of the most interesting features of this project is its additional security image mechanism.

1. Password Strength Validation

The application checks that every newly created account password contains:

- At least 8 characters.
- One uppercase letter (A-Z).
- One lowercase letter (a-z).
- One numerical digit (0-9).
- One special character.

2. Failed Login Security Capture

When an existing account receives an incorrect password:

1. Authentication fails.
2. The application attempts to access the webcam.
3. A single image is captured.
4. The captured image is encrypted.
5. The encrypted image is saved in the account's security folder.

3. Image Encryption

The application uses:

- Fernet: Authenticated symmetric encryption.
- PBKDF2-HMAC: Derives a 32-byte encryption key from the account password.
- SHA-256: Hashing algorithm used during key derivation.
- Random Salt: A unique 16-byte salt for each captured image.
- 600,000 Iterations: Used during password-based key derivation.

4. Viewing Security Images

After successfully logging in, customers can select:

"5. View Security Images"

The application decrypts the stored images using the account password and displays them through OpenCV.

Press "ESC" to stop viewing the images.

---

🧾 Automatic Transaction Receipts

Every successful deposit or withdrawal generates a transaction receipt automatically.

Receipts are stored inside the "receipts/" directory.

Example Folder Structure:
```
receipts/
│
├── receipt_ACC1001_20261114_102500.txt
├── receipt_ACC1001_20261114_103000.txt
└── receipt_ACC1002_20261114_104500.txt
```
Each receipt contains:

- Bank name
- Transaction date and time
- Customer name
- Customer ID
- Account number
- Transaction type
- Transaction amount
- Updated account balance

---

🧪 Automated Testing

The project includes a dedicated security test file:
```
"test_security_alerts.py"
```
The tests use Python's built-in "unittest" framework.

Running the Tests

From the project directory, execute:
```
python -m unittest -v test_security_alerts.py
```
What Is Tested?

The automated tests verify:

1. Successful encryption and decryption of security images.
2. Rejection of an incorrect password during image decryption.
3. Encrypted image storage inside the correct account directory.
4. Webcam image capture and encrypted storage.
5. Security image capture being triggered after an incorrect login password.

These tests also use mocking to simulate webcam behavior without requiring an actual camera for the camera-capture test.

---

📁 Data Storage & Important Notes

- Account information and balances are currently maintained in memory.
- Account records are not permanently saved to a database or file.
- Account information resets when the application terminates.
- Transaction receipts are saved as text files.
- Security images are saved in encrypted ".enc" files.
- Security images are decrypted only when an authenticated customer requests to view them.

Privacy Notice: A failed password attempt for an existing account triggers an attempt to capture one image using the available webcam. The application displays this notice when it starts.

Important: This is an educational banking simulation, not a production banking or financial application. It does not connect to real bank accounts or process actual financial transactions.

---

🐛 Troubleshooting

Camera Not Opening?

- Make sure your webcam is connected.
- Check whether another application is using the camera.
- Verify your operating system's camera permissions.

Missing OpenCV?

Install the required dependencies:
```
python -m pip install -r requirements.txt
```
Missing Cryptography Package?
```
python -m pip install cryptography
```
Security Image Cannot Be Decrypted?

- Make sure you are using the correct account password.
- Ensure the encrypted image file is not corrupted.

Invalid Password?

Make sure your password meets all the strength requirements during account creation.

---

🔒 Privacy & Security

This project implements several security-related mechanisms:

- Password validation before account creation.
- Password authentication before account access.
- Encrypted storage of captured security images.
- Password-derived encryption keys with random salts.
- Account-specific security image directories.
- Local storage of transaction receipts and security images.

Important security consideration: This is a learning project. Account passwords are currently held in memory as plaintext, and account data is not persistently stored. Additional protections would be needed before using a system like this in a real banking environment.

---

📜 License

This project is distributed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this project according to the license terms.

---

👨‍💻 Author

Muhammad Nabeel Rafique

- 🐙 GitHub: "Muhammad-Nabeel-Rafique" (https://github.com/Muhammad-Nabeel-Rafique)
- 🏦 Project: "Digiskills Bank Limited – CLI Banking System" (https://github.com/Muhammad-Nabeel-Rafique/Mini-Bank-Account)

---

<p align="center">
  <strong>Built with ❤️ using Python</strong>
</p><p align="center">
  ⭐ If you like this project, consider giving it a star on GitHub!
</p>
