from os import name, system
from expense import ExpenseTracker


def main() -> None:
    expense_tracker = ExpenseTracker()

    while True:
        print(expense_tracker.menu)

        match input('I pick: '):
            case '1': expense_tracker.add_expense()
            case '2': expense_tracker.view_expenses()
            case '3': expense_tracker.edit_expense()
            case '4': expense_tracker.delete_expense()
            case '5': expense_tracker.filter_by_category()
            case '6': expense_tracker.total_spending()
            case '7': expense_tracker.monthly_budget()
            case '8': print('Exiting Expense Tracker, Goodbye!'); break
            case _: print('Invalid choice. Please enter 1,2, or 3.\n')

if __name__ == '__main__':
    if name == 'nt': system('cls')
    if name == 'posix': system('clear')
    main()
