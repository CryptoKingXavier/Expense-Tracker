from datetime import datetime
from typing import Mapping

class ExpenseTracker(object):

    # DONE: Initialize Tracker
    def __init__(self) -> None:
        self.menu: str = "\nExpense Tracker Menu: \n1. Add Expense \n2. View Expenses \n3. Update Expense \n4. Delete Expense \n5. Filter Category \n6. Total Spending \n7. Monthly Budget \n8. Exit"
        self.data: Mapping[str, list[Mapping[str, str]]] = {
            'expenses': list()
        }
        self.monthly_budget: float = float()

    # DONE: Add Expense: allows users to enter details for name, category, amount, and description
    def add_expense(self) -> None:
        print('Tracking new expense:')
        expense: Mapping[str, str] = {
            'date': f'{datetime.now().year}/{datetime.now().month}/{datetime.now().day}',
            'name': input('\tEnter name: ').strip().title(),
            'category': input('\tEnter the category: ').strip().title(),
            'amount': f'${float(input('\tEnter the amount: ').strip()):,.2f}',
            'description': input('\tEnter a description: ').strip().lower()
        }
        self.data['expenses'].append(expense)
        self.data['expenses'] = sorted(self.data['expenses'], key=lambda item: item['name'])
        print('Expense added successfully!\n')

    # DONE: View Expenses: display a list of all expenses with relevant details
    def view_expenses(self) -> None:
        if self.data and self.data['expenses']:
            print('Viewing Expenses')
            for id, expense in enumerate(self.data['expenses']):
                print(f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']}')
        else:
            print('No expenses recorded yet!\n')

    # DONE: Edit Expenses: enable users to modify details of an existing expense
    def edit_expense(self) -> None:
        self.view_expenses()
        id: int = int(input('\nEnter number to edit: '))
        if self.data and self.data['expenses']:
            for idx, expense in enumerate(self.data['expenses']):
                if idx+1 == id:
                    print('Press `Enter` to use default entry!')
                    new_name: str = input('\tEnter new name: ')
                    new_category: str = input('\tEnter the category: ').strip().title()
                    new_amount: str = f'${float(input('\tEnter the amount: ').strip()):,.2f}'
                    expense['name'] = expense['name'] if not new_name else new_name
                    expense['category'] = expense['category'] if not new_category else new_category
                    expense['amount'] = expense['amount'] if not new_amount else new_amount
            print('Expense updated successfully!\n')

    # DONE: Delete Expense: allow users to remove an expense from the tracker
    def delete_expense(self) -> None:
        id: int = int(input('Enter number to delete: '))
        if self.data and self.data['expenses']:
            for idx, expense in enumerate(self.data['expenses']):
                self.data['expenses'].remove(expense) if idx+1 == id else None
            print('Expense removed successfully!\n')

    # DONE: Expense Categories: categorize expenses and summarize expenses by category
    def filter_by_category(self) -> None:
        if self.data and self.data['expenses']:
            categories: list[str] = list()

            for expense in self.data['expenses']:
                if expense['category'] not in categories: categories.append(expense['category'])

            print(f'Category List: {categories}')
            category: str = input('\tEnter category name to filter: ').strip()

            print(f'\nExpenses in {category.title()} Category')
            for id, expense in enumerate(self.data['expenses']):
                if expense['category'] == category.title():
                    print(f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']}')

    # DONE: Expense Categories: categorize expenses and summarize expenses by date range
    def filter_by_date_range(self, callback: bool | None = None) -> None:
        if self.data and self.data['expenses']:
            filtered_expenses: list[Mapping[str, str]] = list()
            start_date = datetime.strptime(input('Enter start date (YYYY/MM/DD): '), '%Y/%m/%d').date()
            end_date = datetime.strptime(input('Enter end date (YYYY/MM/DD): '), '%Y/%m/%d').date()

            for expense in self.data['expenses']:
                expense_date = datetime.strptime(expense['date'], '%Y/%m/%d').date()
                if start_date <= expense_date <= end_date:
                    filtered_expenses.append(expense)

            if callback is None:
                print(f'\nExpenses between {start_date} and {end_date}')
                for id, expense in enumerate(filtered_expenses):
                    print(f'\t{id+1}. {expense['name']} | {expense['category']} | {expense['amount']}')
            if callback is not None:
                return [start_date, end_date, filtered_expenses]

    # DONE: Total spending: Calculate and display the total spending over a specific period
    def total_spending(self) -> None:
        start_date, end_date, filtered_expenses = self.filter_by_date_range(callback=not(None))
        total_expenses: float = float()

        for expense in filtered_expenses:
            total_expenses += float(expense['amount'].replace('$', '').replace(',', ''))
        
        print(f'Total Expenses between {start_date} and {end_date} is: ${total_expenses:,.2f}')

    # DONE: Monthly Budget: Set a monthly budget and compare it with actual spending
    def monthly_budget(self) -> None:
        if self.data and self.data['expenses']:
            self.monthly_budget = float(input('Enter monthly budget: '))
            total_expenses: float = float()

            for expense in self.data['expenses']:
                total_expenses += float(expense['amount'].replace('$', '').replace(',', ''))

            turnover: float = self.monthly_budget - total_expenses

            print(f'Monthly Budget Deficit Amount: ${turnover:,.2f}') if turnover < 0 else print(f'Monthly Budget Surplus Amount: ${turnover:,.2f}') if turnover > 0 else print('Monthly Budget Has Broken Even!')
