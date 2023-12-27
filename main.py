from os import name, system
from expense import ExpenseTracker

def main() -> None:
    expense_tracker: ExpenseTracker = ExpenseTracker()

    while True:
        expense_tracker.get_menu()

        ExpenseTracker.color_format(_input=not(None))
        match input('I pick: '):
            case '1': expense_tracker.add_expense()
            case '2': expense_tracker.view_expenses()
            case '3': expense_tracker.edit_expense()
            case '4': expense_tracker.delete_expense()
            case '5': expense_tracker.filter_by_category()
            case '6': expense_tracker.total_spending()
            case '7': expense_tracker.monthly_budget()
            case '8': expense_tracker.export_to_csv()
            case '9': expense_tracker.import_from_csv()
            case '10': ExpenseTracker.color_format(_print=not(None), data='Exiting Expense Tracker, Goodbye!'); break
            case _: ExpenseTracker.color_format(_print=not(None), data='Invalid choice. Please enter 1,2,3,...,10\n')

if __name__ == '__main__':
    system('cls') if name == 'nt' else system('clear')
    main()
