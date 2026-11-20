# Personal Expense Tracker (Python + SQLite)

A command-line Python application to record daily expenses, store them in a local SQLite database, view transactions, generate monthly and category-wise summaries, delete an entry, and export records to CSV.

## Features
1. Add an expense with date, category, description, and amount.
2. View all saved expenses.
3. Generate a monthly summary grouped by category.
4. Generate an overall category-wise summary.
5. Delete an expense using its ID.
6. Export saved expenses to `expenses_export.csv`.

## Technology
- Python 3
- SQLite (`sqlite3` standard library)
- CSV (`csv` standard library)

No third-party Python packages are required.

## Requirements
- Python 3.8 or later
- Windows, macOS, or Linux terminal

## How to run
1. Download or extract this project folder.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python expense_tracker.py
   ```

   On some Windows installations, use `py expense_tracker.py`.

4. Choose an option from the menu.
5. The program automatically creates `expenses.db` in the same folder. Your records remain saved when you close and reopen the application.

## Date and amount format
- Date: `YYYY-MM-DD` (for example, `2026-11-20`). Leave the date blank to use today's date.
- Amount: enter a positive number, such as `125.50`.

## Project structure
```text
Expense_Tracker_Project/
├── expense_tracker.py
├── README.md
└── Project_Report.pdf
```

The database and CSV export are generated when you run the application; they are not included as pre-filled user data.

## Example test
1. Select `1` and add: date `2026-11-20`, category `Food`, description `Lunch`, amount `120`.
2. Add another expense: category `Travel`, description `Bus fare`, amount `30`.
3. Select `2` to view both records.
4. Select `3` and enter `2026-11` to view that month's summary.
5. Select `6` to create `expenses_export.csv`.

## Database design
The `expenses` table contains:
- `id`: auto-incremented primary key
- `expense_date`: expense date stored as text in ISO format
- `category`: expense category
- `description`: short explanation
- `amount`: positive numeric amount

## Limitations and future improvements
This is a console-based learning project. Possible improvements include a graphical interface, budget limits, charts, recurring expenses, user login, and cloud synchronization.

## Author
Aastha Vilas Patil
