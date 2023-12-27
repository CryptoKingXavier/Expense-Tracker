from os.path import isfile
from typing import Mapping
from datetime import datetime
from csv import writer, reader
from colorama import init, Fore, Style

class ExpenseTracker(object):

    def __init__(self) -> None:
        """Initialize ExpenseTracker Class"""        
        init()   # Initialize the colorama syntax highlighting class
        self.set_currency()
        self.currency: str | None = None
        self.monthly_budget: float = float()
        self.data: Mapping[str, list[Mapping[str, str]]] = {
            'expenses': list()
        }
        self.menu: str = "\nExpense Tracker Menu: \n1. Add Expense \n2. View Expenses \n3. Update Expense \n4. Delete Expense \n5. Filter Category \n6. Total Spending \n7. Monthly Budget \n8. Export to CSV \n9. Import from CSV \n10. Exit"

    def get_menu(self) -> None:
        """Get Menu Content"""        
        print(Fore.MAGENTA + self.menu + Style.RESET_ALL + '\n')

    @classmethod
    def color_format(cls, _input: bool | None = None, _print: bool | None = None, data: str = '', _error: bool | None = None) -> None:
        """Color Syntax Highlighting

        Args:
            _input (bool | None, optional): Parameter to style the input function. Defaults to None.
            _print (bool | None, optional): Parameter to style the print function. Defaults to None.
            data (str, optional): Parameter used in the print function. Defaults to ''.
            _error (bool | None, optional): Parameter to style the Exception Error Handling. Defaults to None.
        """        
        # Formatting Input Prompts
        if _input is not None: print(Fore.CYAN)
        # Formatting Print Messages
        if _print is not None: print(Fore.BLUE + data + Style.RESET_ALL)
        # Formatting Error Messages
        if _error is not None: print(Fore.RED + data + Style.RESET_ALL)

    def set_currency(self) -> None:
        """Set Currency Denomination: USD/GBP/EUR/YEN"""        
        ExpenseTracker.color_format(_input=not(None))
        currency: str = input('Pick Default Currency (NGN/USD/GBP/EUR/YEN): ').strip().lower()
        match currency:
            case 'usd': self.currency = '$'
            case 'eur': self.currency = '€'
            case 'gbp': self.currency = '£'
            case 'yen': self.currency = '¥'
            case _: self.currency = '₦'
        ExpenseTracker.color_format(_print=not(None), data=f'Default Currency is {self.currency}')

    def add_expense(self) -> None:
        """Add Expense: allows users to enter details for name, category, amount, and description"""        
        ExpenseTracker.color_format(_print=not(None), data='Tracking new expense:')
        ExpenseTracker.color_format(_input=not(None))
        expense: Mapping[str, str] = {
            'date': f'{datetime.now().year}/{datetime.now().month}/{datetime.now().day}',
            'name': input('\tEnter name: ').strip().title(),
            'category': input('\tEnter the category: ').strip().title(),
            'amount': f'{self.currency}{float(input('\tEnter the amount: ').strip()):,.2f}',
            'description': input('\tEnter a description: ').strip().lower()
        }
        self.data['expenses'].append(expense)
        self.data['expenses'] = sorted(self.data['expenses'], key=lambda item: item['name'])
        ExpenseTracker.color_format(_print=not(None), data='Expense added successfully!\n')

    def view_expenses(self) -> None:
        """View Expenses: display a list of all expenses with relevant details"""        
        if self.data and self.data['expenses']:
            ExpenseTracker.color_format(_print=not(None), data='Viewing Expenses')
            for id, expense in enumerate(self.data['expenses']):
                ExpenseTracker.color_format(_print=not(None), data=f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']} | {expense['description']}')
        else:
            ExpenseTracker.color_format(_print=not(None), data='No expenses recorded yet!\n')

    def edit_expense(self) -> None:
        """Edit Expenses: enable users to modify details of an existing expense"""        
        self.view_expenses()
        ExpenseTracker.color_format(_input=not(None))
        id: int = int(input('\nEnter number to edit: '))
        if self.data and self.data['expenses']:
            for idx, expense in enumerate(self.data['expenses']):
                if idx+1 == id:
                    ExpenseTracker.color_format(_print=not(None), data='Press `Enter` to use default entry!')
                    ExpenseTracker.color_format(_input=not(None))
                    new_name: str = input('\tEnter new name: ')
                    new_category: str = input('\tEnter the category: ').strip().title()
                    new_amount: str = f'{self.currency}{float(input('\tEnter the amount: ').strip()):,.2f}'
                    expense['name'] = expense['name'] if not new_name else new_name
                    expense['category'] = expense['category'] if not new_category else new_category
                    expense['amount'] = expense['amount'] if not new_amount else new_amount
            ExpenseTracker.color_format(_print=not(None), data='Expense updated successfully!\n')

    def delete_expense(self) -> None:
        """Delete Expense: allow users to remove an expense from the tracker"""        
        ExpenseTracker.color_format(_input=not(None))
        id: int = int(input('Enter number to delete: '))
        if self.data and self.data['expenses']:
            for idx, expense in enumerate(self.data['expenses']):
                self.data['expenses'].remove(expense) if idx+1 == id else None
            ExpenseTracker.color_format(_print=not(None), data='Expense removed successfully!\n')

    def filter_by_category(self) -> None:
        """Expense Categories: categorize expenses and summarize expenses by category"""        
        if self.data and self.data['expenses']:
            categories: list[str] = list()

            for expense in self.data['expenses']:
                if expense['category'] not in categories: categories.append(expense['category'])

            ExpenseTracker.color_format(_print=not(None), data=f'Category List: {categories}')
            ExpenseTracker.color_format(_input=not(None))
            category: str = input('\tEnter category name to filter: ').strip()

            ExpenseTracker.color_format(_print=not(None), data=f'\nExpenses in {category.title()} Category')
            for id, expense in enumerate(self.data['expenses']):
                if expense['category'] == category.title():
                    ExpenseTracker.color_format(_print=not(None), data=f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']} | {expense['description']}')

    def filter_by_date_range(self, callback: bool | None = None) -> None:
        """Expense Categories: categorize expenses and summarize expenses by date range

        Args:
            callback (bool | None, optional): Checks for external function call. Defaults to None.
        """        
        if self.data and self.data['expenses']:
            filtered_expenses: list[Mapping[str, str]] = list()
            ExpenseTracker.color_format(_input=not(None))
            start_date = datetime.strptime(input('Enter start date (YYYY/MM/DD): '), '%Y/%m/%d').date()
            end_date = datetime.strptime(input('Enter end date (YYYY/MM/DD): '), '%Y/%m/%d').date()

            for expense in self.data['expenses']:
                expense_date = datetime.strptime(expense['date'], '%Y/%m/%d').date()
                if start_date <= expense_date <= end_date:
                    filtered_expenses.append(expense)

            if callback is None:
                ExpenseTracker.color_format(_print=not(None), data=f'\nExpenses between {start_date} and {end_date}')
                for id, expense in enumerate(filtered_expenses):
                    ExpenseTracker.color_format(_print=not(None), data=f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']} | {expense['description']}')
            if callback is not None:
                return [start_date, end_date, filtered_expenses]

    def total_spending(self) -> None:
        """Total spending: Calculate and display the total spending over a specific period"""        
        start_date, end_date, filtered_expenses = self.filter_by_date_range(callback=not(None))
        total_expenses: float = float()

        for expense in filtered_expenses:
            total_expenses += float(expense['amount'].replace(self.currency, '').replace(',', ''))
        
        ExpenseTracker.color_format(_print=not(None), data=f'Total Expenses between {start_date} and {end_date} is: {self.currency}{total_expenses:,.2f}')

    def monthly_budget(self) -> None:
        """Monthly Budget: Set a monthly budget and compare it with actual spending"""        
        if self.data and self.data['expenses']:
            self.monthly_budget = float(input('Enter monthly budget: '))
            total_expenses: float = float()

            for expense in self.data['expenses']:
                total_expenses += float(expense['amount'].replace(self.currency, '').replace(',', ''))

            turnover: float = self.monthly_budget - total_expenses
            
            ExpenseTracker.color_format(_print=not(None), data=f'Monthly Budget Deficit Amount: {self.currency}{turnover:,.2f}') if turnover < 0 else ExpenseTracker.color_format(_print=not(None), data=f'Monthly Budget Surplus Amount: {self.currency}{turnover:,.2f}') if turnover > 0 else ExpenseTracker.color_format(_print=not(None), data='Monthly Budget Has Broken Even!')

    def export_to_csv(self) -> None:
        """Export Data: User's optional request to export to CSV"""        
        ExpenseTracker.color_format(_input=not(None))
        output_file: str = input('Name of output file: ')
        export_data: list[list[str]] = list()

        for expense in self.data['expenses']:
            export_data.append(list(expense.values()))

        for expense in export_data:
            expense[3]: str = expense[3].replace(self.currency, '')

        try:
            with open(output_file, 'w', newline='') as expenses_file:
                expense_writer = writer(expenses_file)
                expense_writer.writerows(export_data)
                expenses_file.close()
                ExpenseTracker.color_format(_print=not(None), data=f'Successfully exported data to {output_file}!')
        except Exception:
            ExpenseTracker.color_format(_error=not(None), data=f'Data Export Error!')

    def import_from_csv(self) -> None:
        """Import Data: User's optional request to import from CSV"""        
        ExpenseTracker.color_format(_input=not(None))
        input_file: str = input('Name of input file: ')
        imported_data: list[Mapping[str, str]] = list()

        if isfile(input_file):
            try:
                with open(input_file, 'r') as expenses_file:
                    expense_reader = reader(expenses_file)
                    for row in expense_reader:
                        row[3]: str = f'{self.currency}{row[3]}'
                        temp_dict: Mapping[str, str] = dict(zip(
                            ['date', 'name', 'category', 'amount', 'description'],
                            list(row)
                        ))
                        imported_data.append(temp_dict)
                    expenses_file.close()
                    self.data['expenses'].extend(imported_data)
                    ExpenseTracker.color_format(_print=not(None), data=f'Successfully imported data from {input_file}!')
            except Exception:
                ExpenseTracker.color_format(_error=not(None), data=f'Data Import Error!')
