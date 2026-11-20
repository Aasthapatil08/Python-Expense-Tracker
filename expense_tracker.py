"""
Expense Tracker - Python + SQLite
A beginner-friendly command-line application to record and analyze expenses.

Run:
    python expense_tracker.py

The database file (expenses.db) is created automatically in this folder.
"""

import csv
import sqlite3
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).with_name("expenses.db")
DATE_FORMAT = "%Y-%m-%d"


def connect_db():
    """Open a database connection and ensure the expenses table exists."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0)
        )
        """
    )
    connection.commit()
    return connection


def valid_date(value):
    """Return a normalized YYYY-MM-DD date, or None if invalid."""
    try:
        parsed = datetime.strptime(value.strip(), DATE_FORMAT).date()
        if parsed > date.today():
            return None
        return parsed.isoformat()
    except ValueError:
        return None


def add_expense():
    print("\n--- Add Expense ---")
    raw_date = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
    expense_date = date.today().isoformat() if not raw_date else valid_date(raw_date)
    if not expense_date:
        print("Invalid date. Use YYYY-MM-DD and do not enter a future date.")
        return

    category = input("Category (e.g. Food, Travel, Bills): ").strip().title()
    description = input("Description: ").strip()
    raw_amount = input("Amount (₹): ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    try:
        amount = round(float(raw_amount), 2)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid amount greater than zero.")
        return

    with connect_db() as connection:
        connection.execute(
            "INSERT INTO expenses (expense_date, category, description, amount) VALUES (?, ?, ?, ?)",
            (expense_date, category, description, amount),
        )
    print("Expense saved successfully.")


def view_expenses():
    print("\n--- All Expenses ---")
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT id, expense_date, category, description, amount "
            "FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()

    if not rows:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Description':<25} {'Amount (₹)':>12}")
    print("-" * 74)
    for row in rows:
        expense_id, expense_date, category, description, amount = row
        print(f"{expense_id:<5} {expense_date:<12} {category[:14]:<15} "
              f"{description[:24]:<25} {amount:>12.2f}")


def monthly_summary():
    print("\n--- Monthly Summary ---")
    month = input("Enter month (YYYY-MM), leave blank for current month: ").strip()
    if not month:
        month = date.today().strftime("%Y-%m")
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT category, COUNT(*), SUM(amount)
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            """,
            (month,),
        ).fetchall()

    if not rows:
        print(f"No expenses found for {month}.")
        return

    total = sum(row[2] for row in rows)
    print(f"\nSummary for {month}")
    print(f"{'Category':<20} {'Transactions':>12} {'Total (₹)':>14}")
    print("-" * 48)
    for category, count, amount in rows:
        print(f"{category:<20} {count:>12} {amount:>14.2f}")
    print("-" * 48)
    print(f"{'Grand Total':<20} {'':>12} {total:>14.2f}")


def category_summary():
    print("\n--- Category-wise Summary ---")
    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT category, COUNT(*), SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
            """
        ).fetchall()

    if not rows:
        print("No expenses recorded yet.")
        return

    print(f"{'Category':<22} {'Transactions':>12} {'Total (₹)':>14}")
    print("-" * 50)
    for category, count, amount in rows:
        print(f"{category:<22} {count:>12} {amount:>14.2f}")


def delete_expense():
    print("\n--- Delete Expense ---")
    raw_id = input("Enter the expense ID to delete: ").strip()
    if not raw_id.isdigit():
        print("Please enter a numeric ID.")
        return

    with connect_db() as connection:
        cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (int(raw_id),))
        deleted = cursor.rowcount

    print("Expense deleted." if deleted else "No expense found with that ID.")


def export_csv():
    print("\n--- Export Expenses ---")
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT id, expense_date, category, description, amount "
            "FROM expenses ORDER BY expense_date, id"
        ).fetchall()

    if not rows:
        print("No expenses available to export.")
        return

    output_path = Path(__file__).with_name("expenses_export.csv")
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Category", "Description", "Amount (INR)"])
        writer.writerows(rows)

    print(f"CSV exported successfully: {output_path.name}")


def show_menu():
    print("\n" + "=" * 42)
    print("           PERSONAL EXPENSE TRACKER")
    print("=" * 42)
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. Monthly expense summary")
    print("4. Category-wise summary")
    print("5. Delete an expense")
    print("6. Export expenses to CSV")
    print("0. Exit")
    print("-" * 42)


def main():
    # Create the database/table before showing the menu.
    with connect_db():
        pass

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            export_csv()
        elif choice == "0":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 0 to 6.")


if __name__ == "__main__":
    main()
