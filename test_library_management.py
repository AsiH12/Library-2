import os
import pytest
from library_management import BooksDAL, CustomersDAL, LoansDAL, main

@pytest.fixture
def setup_test_environment():
    # Ensure clean test environment before running tests
    yield
    try:
        os.remove("test_books.json")
        os.remove("test_customers.json")
        os.remove("test_loans.json")
    except FileNotFoundError:
        pass

def test_add_customer(setup_test_environment, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "John Doe\nCity\n25")
    books_dal = BooksDAL("test_books.json")
    customers_dal = CustomersDAL("test_customers.json")
    loans_dal = LoansDAL("test_loans.json")

    assert len(customers_dal.customers) == 0
    main(books_dal, customers_dal, loans_dal)
    assert len(customers_dal.customers) == 1
    captured = capsys.readouterr()
    assert "Customer added successfully." in captured.out

def test_add_book(setup_test_environment, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "Book Name\nAuthor\n2000\n1")
    books_dal = BooksDAL("test_books.json")
    customers_dal = CustomersDAL("test_customers.json")
    loans_dal = LoansDAL("test_loans.json")

    assert len(books_dal.books) == 0
    main(books_dal, customers_dal, loans_dal)
    assert len(books_dal.books) == 1
    captured = capsys.readouterr()
    assert "Book added successfully." in captured.out

def test_loan_book(setup_test_environment, monkeypatch, capsys):
    customers_dal = CustomersDAL("test_customers.json")
    books_dal = BooksDAL("test_books.json")
    loans_dal = LoansDAL("test_loans.json")

    customers_dal.customers = [{"ID": 1, "Name": "John Doe", "City": "City", "Age": 25}]
    books_dal.books = [{"ID": 1, "Name": "Book Name", "Author": "Author", "YearPublished": 2000, "Type": 1}]

    monkeypatch.setattr("builtins.input", lambda _: "1\n1")
    assert len(loans_dal.loans) == 0
    main(books_dal, customers_dal, loans_dal)
    assert len(loans_dal.loans) == 1
    captured = capsys.readouterr()
    assert "Book loaned successfully." in captured.out

def test_return_book(setup_test_environment, monkeypatch, capsys):
    loans_dal = LoansDAL("test_loans.json")

    loans_dal.loans = [{"CustID": 1, "BookID": 1, "LoanDate": "2023-01-01", "ReturnDate": "2023-01-10"}]

    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert len(loans_dal.loans) == 1
    main(BooksDAL(), CustomersDAL(), loans_dal)
    assert len(loans_dal.loans) == 0
    captured = capsys.readouterr()
    assert "Book returned successfully" in captured.out
