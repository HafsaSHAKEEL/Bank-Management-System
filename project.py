import datetime
import os


class UserActions:
    def __init__(self):
        self.owner_id = None
        self.name = None
        self.age = None
        self.salary = None
        self.account_number = None
        self.pin = None
        self.balance = 0
        self.transaction_history = []

    def prompt_user_info(self, candidate_name):
        self.owner_id = input("Enter your owner ID: ")
        self.name = candidate_name
        self.age = int(input("Enter your age: "))
        self.salary = float(input("Enter your salary: "))
        self.account_number = input("Enter your account number: ")
        self.pin = input("Enter your PIN: ")[::-1]  # reversing pin for encryption
        self.save_to_file()

    def is_account_frozen(self):
        if not os.path.exists("frozen_accounts.txt"):
            return False
        with open("frozen_accounts.txt", "r") as f:
            frozen_accounts = f.read().splitlines()
        return self.account_number in frozen_accounts

    def add_transaction(self, transaction_type, amount, recipient_account=None):
        if self.is_account_frozen():
            self.log_action("Add Transaction", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        transaction = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "recipient": recipient_account,
        }
        self.transaction_history.append(transaction)
        self.save_to_file()
        self.log_action(
            "Add Transaction",
            f"Type: {transaction_type},"
            f" Amount: {amount}, "
            f"Recipient: {recipient_account}",
        )

    def deposit_amount(self, amount):
        if self.is_account_frozen():
            self.log_action("Deposit", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            if amount <= 0:
                raise ValueError(
                    "Invalid deposit amount. Amount must be greater than zero."
                )
            self.balance += amount
            self.add_transaction("Deposit", amount)
            print(
                f"Successful deposit of ${amount:.2f}. Current balance is: ${self.balance:.2f}"
            )
            self.log_action("Deposit", f"Amount: {amount}, New Balance: {self.balance}")
        except ValueError as e:
            self.log_action("Deposit", f"Failed - {e}")
            print(e)
        except Exception as e:
            self.log_action("Deposit", f"Failed - {str(e)}")
            print("OOPS! An unexpected error occurred:", str(e))

    def check_amount(self):
        if self.is_account_frozen():
            self.log_action("Check Balance", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        print(f"Your current balance is: ${self.balance:.2f}")
        self.log_action("Check Balance", f"Current Balance: {self.balance}")

    def print_statement(self):
        if self.is_account_frozen():
            self.log_action("Print Statement", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            print(f"Statement for Account Number {self.account_number}:")
            if not self.transaction_history:
                print("No transactions found for corresponding account number.")
            else:
                for transaction in self.transaction_history:
                    print(
                        f"{transaction['date']}: {transaction['type']}, ${transaction['amount']:.2f}"
                    )
            self.log_action("Print Statement", "Success")
        except Exception as e:
            self.log_action("Print Statement", f"Failed - {e}")
            print(f"Error: {e}")

    def transfer_amount(self, recipient, amount):
        if self.is_account_frozen():
            self.log_action("Transfer", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            if amount <= 0:
                raise ValueError(
                    "INVALID transfer amount. Amount must be greater than zero."
                )
            if self.balance >= amount:
                self.balance -= amount
                recipient.balance += amount
                self.add_transaction("Transfer", amount, recipient.account_number)
                print(
                    f"Transfer of ${amount:.2f} to {recipient.account_number} is successful."
                )
                self.log_action(
                    "Transfer",
                    f"Amount: {amount}, Recipient: {recipient.account_number}",
                )
            else:
                raise ValueError("Insufficient balance for transfer.")
        except ValueError as e:
            self.log_action("Transfer", f"Failed - {e}")
            print(f"Error: {e}")

    def withdraw(self, amount):
        if self.is_account_frozen():
            self.log_action("Withdraw", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            if amount <= 0:
                raise ValueError(
                    "Invalid withdrawal amount. Amount must be greater than zero."
                )
            if self.balance >= amount:
                self.balance -= amount
                self.add_transaction("Withdrawal", amount)
                print(
                    f"Withdrawal of ${amount:.2f} is successful. Now, the Current balance is: ${self.balance:.2f}"
                )
                self.log_action(
                    "Withdraw", f"Amount: {amount}, New Balance: {self.balance}"
                )
            else:
                raise ValueError("Insufficient balance.")
        except ValueError as e:
            self.log_action("Withdraw", f"Failed - {e}")
            print(f"Error: {e}")

    def change_pin(self):
        if self.is_account_frozen():
            self.log_action("Change PIN", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            current_pin = input("Enter your current PIN: ")
            if self.pin != current_pin[::-1]:
                raise ValueError("Current PIN is incorrect.")
            new_pin = input("Please enter your new PIN: ")
            if len(new_pin) != 4:
                raise ValueError("PIN must be exactly 4 digits!")
            self.pin = new_pin[::-1]
            print("PIN changed successfully.")
            self.save_to_file()
            self.log_action("Change PIN", "Success")
        except ValueError as e:
            self.log_action("Change PIN", f"Failed - {e}")
            print(f"Error: {e}")
        except Exception as e:
            self.log_action("Change PIN", f"Failed - {str(e)}")
            print("An unexpected error occurred:", str(e))

    def show_transaction_history(self):
        if self.is_account_frozen():
            self.log_action("Show Transaction History", f"Failed - Account is frozen")
            print(
                "Sorry, your account is frozen. Contact admin to unfreeze the account."
            )
            return
        try:
            print(f"Transaction History for Account Number: {self.account_number}:")
            if not self.transaction_history:
                print("No transactions found:(")
            else:
                for transaction in self.transaction_history:
                    print(
                        f"{transaction['date']}: {transaction['type']}, ${transaction['amount']:.2f}"
                    )
            self.log_action("Show Transaction History", "Success")
        except Exception as e:
            self.log_action("Show Transaction History", f"Failed - {e}")
            print(f"Error: {e}")

    def save_to_file(self):
        account_details = {
            "owner_id": self.owner_id,
            "name": self.name,
            "age": self.age,
            "salary": self.salary,
            "account_number": self.account_number,
            "pin": self.pin,
            "balance": self.balance,
            "transaction_history": self.transaction_history,
        }
        filename = f"account_{self.account_number}.txt"
        with open(filename, "w") as f:
            for k, val in account_details.items():
                f.write(f"{k}: {val}\n")

    def log_action(self, action, details):
        filename = f"log_{self.account_number}.txt"
        with open(filename, "a") as f:
            f.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}: {details}\n"
            )

    @classmethod
    def read_from_file(cls, account_number):
        filename = f"account_{account_number}.txt"
        try:
            with open(filename, "r") as f:
                account_data = {}
                for line in f:
                    key, value = line.strip().split(": ", 1)
                    if key == "transaction_history":
                        account_data[key] = eval(value)
                    elif key in ["age", "balance"]:
                        account_data[key] = float(value) if "." in value else int(value)
                    else:
                        account_data[key] = value

                account = cls()
                account.owner_id = account_data["owner_id"]
                account.name = account_data["name"]
                account.age = account_data["age"]
                account.salary = account_data["salary"]
                account.account_number = account_data["account_number"]
                account.pin = account_data["pin"]
                account.balance = account_data["balance"]
                account.transaction_history = account_data["transaction_history"]
                return account
        except FileNotFoundError:
            print(f"Account with number {account_number} does not exist.")
            return None
        except Exception as e:
            print(f"Error loading account data: {e}")
            return None


class AdminActions:
    def __init__(self):
        self.accounts = {}
        self.transaction_limits = {}

    def create_account(self):
        try:
            owner_id = input("Enter the owner's ID: ")
            if owner_id in self.accounts:
                print("An account already exists for this owner.")
                return
            name = input("Enter name: ")
            if not name.isalpha():
                raise ValueError("Name must be in string.")
            age = int(input("Enter age: "))
            salary = float(input("Enter salary: "))
            account_number = input("Enter account number: ")
            pin = input("Enter the PIN: ")

            new_account = UserActions()
            new_account.owner_id = owner_id
            new_account.name = name
            new_account.age = age
            new_account.salary = salary
            new_account.account_number = account_number
            new_account.pin = pin[::-1]
            self.accounts[owner_id] = new_account
            new_account.save_to_file()
            print(f"Account '{account_number}' created successfully.")
            self.log_action(
                "Create Account",
                f"Owner ID: {owner_id}, Account Number: {account_number}",
            )
        except ValueError as e:
            self.log_action("Create Account", f"Failed - {e}")
            print(f"Invalid input: {e}")
        except Exception as e:
            self.log_action("Create Account", f"Failed - {str(e)}")
            print(f"An error occurred: {e}")

    def show_account_details(self):
        try:
            account_number = input("Enter the account number to display details: ")
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        if key == "transaction_history":
                            account_data[key] = eval(value)
                        elif key in ["age", "balance", "salary"]:
                            account_data[key] = (
                                float(value) if "." in value else int(value)
                            )
                        else:
                            account_data[key] = value

                    print("Account details: ")
                    print(
                        f"Owner ID: {account_data.get('owner_id', '')}, "
                        f"Name: {account_data.get('name', '')}, "
                        f"Age: {account_data.get('age', '')}, "
                        f"Salary: {float(account_data.get('salary', 0)):.2f}, "
                        f"Account Number: {account_data.get('account_number', '')}"
                    )
                    self.log_action(
                        "Show Account Details", f"Account Number: {account_number}"
                    )

            except FileNotFoundError:
                print(" NO account found. Please create account first.")
                self.log_action(
                    "Show Account Details",
                    f"Failed - Account {account_number} not found",
                )

        except Exception as e:
            self.log_action("Show Account Details", f"Failed - {e}")
            print(f"An error occurred while displaying account details: {e}")

    def show_transactions(self):
        try:
            account_number = input("Enter the account number to fetch transactions: ")
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        if key == "transaction_history":
                            account_data[key] = eval(value)
                            break
                        elif key == "account_number":
                            account_number_from_file = value.strip()
                            if account_number != account_number_from_file:
                                print(
                                    f"Account number '{account_number}' does not match the file content."
                                )
                                self.log_action(
                                    "Show Transactions",
                                    f"Failed - Account number mismatch",
                                )
                                return

                    if "transaction_history" in account_data:
                        print(
                            f"Transaction History for Account Number: {account_number}:"
                        )
                        for transaction in account_data["transaction_history"]:
                            print(
                                f"{transaction['date']}: {transaction['type']}, ${transaction['amount']:.2f}"
                            )
                        self.log_action(
                            "Show Transactions", f"Account Number: {account_number}"
                        )
                    else:
                        print("No transaction history found.")
                        self.log_action(
                            "Show Transactions", f"Failed - No transactions found"
                        )

            except FileNotFoundError:
                print(f"File '{filename}' does not exist.")
                self.log_action(
                    "Show Transactions", f"Failed - File {filename} not found"
                )

        except Exception as e:
            self.log_action("Show Transactions", f"Failed - {e}")
            print(f"An error occurred while fetching transactions: {e}")

    def set_transaction_limit(self, account_number, limit):
        try:
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        account_data[key] = value.strip()

                    if account_data.get("account_number") == account_number:
                        self.transaction_limits[account_number] = limit
                        print(
                            f"Transaction limit for account {account_number} is set to ${limit:.2f}."
                        )
                        self.log_action(
                            "Set Transaction Limit",
                            f"Account Number: {account_number}, Limit: {limit}",
                        )
                    else:
                        print(
                            f"Account number '{account_number}' does not match the file content."
                        )
                        self.log_action(
                            "Set Transaction Limit", f"Failed - Account number mismatch"
                        )

            except FileNotFoundError:
                print("Account not found. Please create an account first.")
                self.log_action(
                    "Set Transaction Limit",
                    f"Failed - Account {account_number} not found",
                )

        except Exception as e:
            self.log_action("Set Transaction Limit", f"Failed - {e}")
            print(f"An error occurred while setting the transaction limit: {e}")

    def freeze_account(self, account_number):
        try:
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        account_data[key] = value.strip()

                    if account_data.get("account_number") == account_number:
                        with open("frozen_accounts.txt", "a") as frozen_file:
                            frozen_file.write(f"{account_number}\n")
                        print(f"Account {account_number} has been frozen.")
                        self.log_action(
                            "Freeze Account", f"Account Number: {account_number}"
                        )
                    else:
                        print(
                            f"Account number '{account_number}' does not match the file content."
                        )
                        self.log_action(
                            "Freeze Account", f"Failed - Account number mismatch"
                        )

            except FileNotFoundError:
                print("Account not found. Please create an account first.")
                self.log_action(
                    "Freeze Account", f"Failed - Account {account_number} not found"
                )

        except Exception as e:
            self.log_action("Freeze Account", f"Failed - {e}")
            print(f"An error occurred while freezing the account: {e}")

    def unfreeze_account(self, account_number):
        try:
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        account_data[key] = value.strip()

                    if account_data.get("account_number") == account_number:
                        if os.path.exists("frozen_accounts.txt"):
                            with open("frozen_accounts.txt", "r") as frozen_file:
                                frozen_accounts = frozen_file.read().splitlines()
                            if account_number in frozen_accounts:
                                frozen_accounts.remove(account_number)
                                with open("frozen_accounts.txt", "w") as frozen_file:
                                    for acc in frozen_accounts:
                                        frozen_file.write(f"{acc}\n")
                                print(f"Account {account_number} has been unfrozen.")
                                self.log_action(
                                    "Unfreeze Account",
                                    f"Account Number: {account_number}",
                                )
                            else:
                                print("Account is not frozen.")
                                self.log_action(
                                    "Unfreeze Account", f"Failed - Account not frozen"
                                )
                        else:
                            print("No frozen accounts found.")
                            self.log_action(
                                "Unfreeze Account", f"Failed - No frozen accounts"
                            )

                    else:
                        print(
                            f"Account number '{account_number}' does not match the file content."
                        )
                        self.log_action(
                            "Unfreeze Account", f"Failed - Account number mismatch"
                        )

            except FileNotFoundError:
                print("Account not found. Please create an account first.")
                self.log_action(
                    "Unfreeze Account", f"Failed - Account {account_number} not found"
                )

        except Exception as e:
            self.log_action("Unfreeze Account", f"Failed - {e}")
            print(f"An error occurred while unfreezing the account: {e}")

    def delete_account(self, account_number):
        try:
            filename = f"account_{account_number}.txt"

            try:
                with open(filename, "r") as f:
                    account_data = {}
                    for line in f:
                        key, value = line.strip().split(": ", 1)
                        account_data[key] = value.strip()

                    if account_data.get("account_number") == account_number:
                        if account_number in self.accounts:
                            del self.accounts[account_number]
                            print(f"Account {account_number} has been deleted.")
                            self.log_action(
                                "Delete Account", f"Account Number: {account_number}"
                            )
                        else:
                            print("Account not found.")
                            self.log_action(
                                "Delete Account",
                                f"Failed - Account {account_number} not found",
                            )
                    else:
                        print(
                            f"Account number '{account_number}' does not match the file content."
                        )
                        self.log_action(
                            "Delete Account", f"Failed - Account number mismatch"
                        )

            except FileNotFoundError:
                print("Account not found. Please create an account first.")
                self.log_action(
                    "Delete Account", f"Failed - Account {account_number} not found"
                )

        except Exception as e:
            self.log_action("Delete Account", f"Failed - {e}")
            print(f"An error occurred while deleting the account: {e}")

    def log_action(self, action, details):
        filename = "admin_log.txt"
        with open(filename, "a") as f:
            f.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}: {details}\n"
            )


def main():
    print("*****************Welcome to the Banking System***********************")
    candidate_name = input("HELLO! Please enter your name First: ")
    user_type = input("Are you a user or an admin? (User/Admin): ")

    if user_type.lower() == "user":
        account_number = input("Please enter your account number: ")
        user = UserActions.read_from_file(account_number)
        if not user:
            print("SORRY, ACCOUNT NOT FOUND, PLEASE CREATE AN ACCOUNT FIRST:)")
            return

        print(f"Welcome, {candidate_name}!")
        display_menu(user)

    elif user_type.lower() == "admin":
        admin = AdminActions()
        print(f"Welcome, Admin {candidate_name}!")
        while True:
            print("\n1. Create Account")
            print("2. Show Account Details")
            print("3. Show Transactions")
            print("4. Set Transaction Limit")
            print("5. Freeze Account")
            print("6. Unfreeze Account")
            print("7. Delete Account")
            print("8. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                admin.create_account()
            elif choice == "2":
                admin.show_account_details()
            elif choice == "3":
                admin.show_transactions()
            elif choice == "4":
                account_number = input("Enter account number: ")
                limit = float(input("Enter transaction limit: "))
                admin.set_transaction_limit(account_number, limit)
            elif choice == "5":
                account_number = input("Enter account number: ")
                admin.freeze_account(account_number)
            elif choice == "6":
                account_number = input("Enter account number: ")
                admin.unfreeze_account(account_number)
            elif choice == "7":
                account_number = input("Enter account number: ")
                admin.delete_account(account_number)
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid user type. Please try again.")


def display_menu(user):
    """
    Display the main menu for the banking system for a user.
    """
    while True:
        print("\n1. Deposit Amount")
        print("2. Check Balance")
        print("3. Print Statement")
        print("4. Transfer Amount")
        print("5. Withdraw Amount")
        print("6. Change PIN")
        print("7. View Transaction History")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            user.deposit_amount(amount)
        elif choice == "2":
            user.check_amount()
        elif choice == "3":
            user.print_statement()
        elif choice == "4":
            recipient_account = input("Enter recipient's account number: ")
            recipient = UserActions.read_from_file(recipient_account)
            if recipient:
                amount = float(input("Enter amount to transfer: "))
                user.transfer_amount(recipient, amount)
        elif choice == "5":
            amount = float(input("Enter amount to withdraw: "))
            user.withdraw(amount)
        elif choice == "6":
            user.change_pin()
        elif choice == "7":
            user.show_transaction_history()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
