import json
from datetime import datetime, timedelta
import os

class BooksDAL:
    def __init__(self, file_path="books.json"):
        self.file_path = file_path
        self.books = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.books, file, indent=2)

    def get_max_loan_days(self, book_type):
        return {1: 10, 2: 5, 3: 2}.get(book_type, 0)

class CustomersDAL:
    def __init__(self, file_path="customers.json"):
        self.file_path = file_path
        self.customers = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.customers, file, indent=2)

class LoansDAL:
    def __init__(self, file_path="loans.json"):
        self.file_path = file_path
        self.loans = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.loans, file, indent=2)

def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def display_menu():
    print("\nLibrary Management System")
    print("1. Add a new customer")
    print("2. Add a new book")
    print("3. Loan a book")
    print("4. Return a book")
    print("5. Display all books")
    print("6. Display all customers")
    print("7. Display all loans")
    print("8. Display late loans")
    print("9. Find book by name")
    print("10. Find customer by name")
    print("11. Remove book")
    print("12. Remove customer")
    print("0. Exit")

def display_books(books):
    print("All books:")
    for book in books:
        print(book)

def display_customers(customers):
    print("All customers:")
    for customer in customers:
        print(customer)

def display_loans(loans):
    print("All loans:")
    for loan in loans:
        print(loan)

def display_late_loans(loans):
    print("Late loans:")
    late_loans = [loan for loan in loans if loan["ReturnDate"] < loan["LoanDate"]]
    for late_loan in late_loans:
        print(late_loan)

def find_book_by_name(books, book_name):
    found_books = [book for book in books if book_name.lower() in book["Name"].lower()]
    print("Found books:")
    for found_book in found_books:
        print(found_book)

def find_customer_by_name(customers, customer_name):
    found_customers = [customer for customer in customers if customer_name.lower() in customer["Name"].lower()]
    print("Found customers:")
    for found_customer in found_customers:
        print(found_customer)

def main(books_dal, customers_dal, loans_dal):
    while True:
        display_menu()
        choice = get_integer_input("Enter your choice: ")

        if choice == 1:
            name = input("Enter customer name: ")
            city = input("Enter customer city: ")
            age = get_integer_input("Enter customer age: ")
            customer_ids = [customer["ID"] for customer in customers_dal.customers]
            new_customer_id = 1 if not customer_ids else max(customer_ids) + 1
            new_customer = {"ID": new_customer_id, "Name": name, "City": city, "Age": age}
            customers_dal.customers.append(new_customer)
            customers_dal.save_data()
            print("Customer added successfully.")

        elif choice == 2:
            name = input("Enter book name: ")
            author = input("Enter book author: ")
            year_published = get_integer_input("Enter year published: ")
            book_type = get_integer_input("Enter book type (1/2/3): ")
            book_ids = [book["ID"] for book in books_dal.books]
            new_book_id = 1 if not book_ids else max(book_ids) + 1
            new_book = {"ID": new_book_id, "Name": name, "Author": author, "YearPublished": year_published, "Type": book_type}
            books_dal.books.append(new_book)
            books_dal.save_data()
            print("Book added successfully.")

        elif choice == 3:
            cust_id = get_integer_input("Enter customer ID: ")
            book_id = get_integer_input("Enter book ID: ")
            book_type = next((book["Type"] for book in books_dal.books if book["ID"] == book_id), None)
            max_loan_days = books_dal.get_max_loan_days(book_type)
            if max_loan_days > 0:
                loan_date = datetime.now().strftime("%Y-%m-%d")
                return_date = (datetime.now() + timedelta(days=max_loan_days)).strftime("%Y-%m-%d")
                new_loan = {"CustID": cust_id, "BookID": book_id, "LoanDate": loan_date, "ReturnDate": return_date}
                loans_dal.loans.append(new_loan)
                loans_dal.save_data()
                print("Book loaned successfully.")
            else:
                print("Invalid book type. Unable to determine maximum loan days.")

        elif choice == 4:
            loan_id = get_integer_input("Enter loan ID to return: ")
            if 1 <= loan_id <= len(loans_dal.loans):
                returned_book = loans_dal.loans.pop(loan_id - 1)
                loans_dal.save_data()
                print(f"Book returned successfully: {returned_book}")
            else:
                print("Invalid loan ID. Please enter a valid ID.")

        elif choice == 5:
            display_books(books_dal.books)

        elif choice == 6:
            display_customers(customers_dal.customers)

        elif choice == 7:
            display_loans(loans_dal.loans)

        elif choice == 8:
            display_late_loans(loans_dal.loans)

        elif choice == 9:
            book_name = input("Enter book name to find: ")
            find_book_by_name(books_dal.books, book_name)

        elif choice == 10:
            customer_name = input("Enter customer name to find: ")
            find_customer_by_name(customers_dal.customers, customer_name)

        elif choice == 11:
            book_id = get_integer_input("Enter book ID to remove: ")
            if 1 <= book_id <= len(books_dal.books):
                del books_dal.books[book_id - 1]
                books_dal.save_data()
                print("Book removed successfully.")
            else:
                print("Invalid book ID. Please enter a valid ID.")

        elif choice == 12:
            customer_id = get_integer_input("Enter customer ID to remove: ")
            if 1 <= customer_id <= len(customers_dal.customers):
                del customers_dal.customers[customer_id - 1]
                customers_dal.save_data()
                print("Customer removed successfully.")
            else:
                print("Invalid customer ID. Please enter a valid ID.")

        elif choice == 0:
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main(BooksDAL(), CustomersDAL(), LoansDAL())
