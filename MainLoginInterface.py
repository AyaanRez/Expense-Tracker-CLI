import os
import json
from datetime import datetime

DATA_STORAGE = "user_data"
README_FILE = "README.txt"

def create_user(username, password):
    user_data = {"username": username, "password": password, "expenses": {}, "income": {}, "budgets": {}}

    with open(os.path.join(DATA_STORAGE, f"{username}.json"), "w") as f:
        json.dump(user_data, f)

def retrieve_user(username):
    with open(os.path.join(DATA_STORAGE, f"{username}.json"), "r") as f:
        return json.load(f)

def upload_data(username, data):
    with open(os.path.join(DATA_STORAGE, f"{username}.json"), "w") as f:
        json.dump(data, f)

def login():
    username = input("Username: ")

    password = input("Password: ")

    user_data_path = os.path.join(DATA_STORAGE, f"{username}.json")

    if os.path.exists(user_data_path):
        with open(user_data_path, "r") as f:
            user_data = json.load(f)
            if user_data["password"] == password:
                return user_data
    return None


def add_transaction(user_data, transaction_type):
    amount = float(input("Amount: "))

    category = input("Category: ")

    label = input("Label: ")

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if transaction_type == "expense":
        if category not in user_data["expenses"]:
            user_data["expenses"][category] = []
        user_data["expenses"][category].append({"amount": amount, "label": label, "date": date})
        
        if category in user_data["budgets"] and sum(expense["amount"] for expense in user_data["expenses"][category]) > user_data["budgets"][category]:
            print("Warning: You have exceeded your budget for this category.")

    elif transaction_type == "income":
        if category not in user_data["income"]:
            user_data["income"][category] = []
        user_data["income"][category].append({"amount": amount, "label": label, "date": date})

    upload_data(user_data["username"], user_data)

    print(f"{transaction_type.capitalize()} added successfully.")

def create_budget(user_data):
    category = input("Category to budget for: ")

    budget_amount = float(input("Budget amount: "))

    user_data["budgets"][category] = budget_amount

    upload_data(user_data["username"], user_data)

    print("Budget created successfully.")

def display_transaction_history(user_data):
    print("Expense History:")

    for category, expenses in user_data["expenses"].items():
        for expense in expenses:
            print(f"Amount: {expense['amount']}, Category: {category}, Label: {expense['label']}, Date: {expense['date']}")

    print("\nIncome History:")

    for category, income in user_data["income"].items():
        for income_item in income:
            print(f"Amount: {income_item['amount']}, Category: {category}, Label: {income_item['label']}, Date: {income_item['date']}")
    
    print("\n1. Clear All Data")

    print("2. Back to Main Menu")

    choice = input("Enter your choice: ")

    if choice == "1":
        confirm = input("Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == "yes":
            clear_all_data(user_data)
            print("All data cleared successfully.")

    elif choice == "2":
        return
    
    else:
        print("Invalid choice.")

def delete_account(user_data):
    username = user_data["username"]

    user_data_path = os.path.join(DATA_STORAGE, f"{username}.json")

    os.remove(user_data_path)

    print("Account deleted successfully.")

def clear_all_data(user_data):
    user_data["expenses"] = {}

    user_data["income"] = {}

    user_data["budgets"] = {}

    upload_data(user_data["username"], user_data)

def display_readme():
    readme_path = os.path.join(os.path.dirname(__file__), README_FILE)
    with open(readme_path, "r") as f:
        print(f.read())

def main():
    if not os.path.exists(DATA_STORAGE):
        os.makedirs(DATA_STORAGE)

    while True:
        print("\n1. Sign Up")

        print("2. Log In")

        print("3. Display README")

        print("4. Exit")

        menu_choice = input("Enter your choice: ")

        if menu_choice == "1":
            username = input("Enter a username: ")

            password = input("Enter a password: ")

            create_user(username, password)

            print("User created successfully.")

        elif menu_choice == "2":
            user_data = login()

            if user_data:
                print("Login successful.")
                while True:
                    print("\n1. Add Expense")

                    print("2. Add Income")

                    print("3. Create Budget")

                    print("4. Display Transaction History")

                    print("5. Delete Account")

                    print("6. Log Out")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        add_transaction(user_data, "expense")

                    elif user_choice == "2":
                        add_transaction(user_data, "income")

                    elif user_choice == "3":
                        create_budget(user_data)

                    elif user_choice == "4":
                        display_transaction_history(user_data)

                    elif user_choice == "5":
                        confirm = input("Are you sure you want to delete your account? This action cannot be undone. (yes/no): ")
                        if confirm.lower() == "yes":
                            delete_account(user_data)
                            break

                    elif user_choice == "6":
                        break

                    else:
                        print("Invalid choice.")
            else:
                print("Invalid username or password.")

        elif menu_choice == "3":
            display_readme()

        elif menu_choice == "4":
            print("Thank you for using Expense Tracker CLI!")
            break
        
        else:
            print("Invalid choice.")

main()