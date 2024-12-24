import csv
import pandas as pd

import sys
from note import NoteManager
from task import TaskManager
from contact import ContactManager
from finance_record import FinanceManager
from func import read_csv, write_csv

class Calculator:

    def calculate(self, expression: str):
        try:
            allowed_chars = '0123456789+-*/.() '
            if not all(char in allowed_chars for char in expression):
                raise ValueError('Выражение содержит недопустимые символы')

            result = eval(expression)
            return result
        except ZeroDivisionError:
            return 'Ошибка: деление на ноль'
        except Exception as er:
            return f'Ошибка: {er}'


class PersonalAssistant:
    def __init__(self):
        self.note_manager = NoteManager()
        self.task_manager = TaskManager()
        self.contact_manager = ContactManager()
        self.finance_manager = FinanceManager()
        self.calculator = Calculator()

        self.menu_options = {
            '1': self.manage_notes,
            '2': self.manage_tasks,
            '3': self.manage_contacts,
            '4': self.manage_financial_records,
            '5': self.manage_calculator,
            '6': self.exit_program
        }

    def display_menu(self):
        print("""
        Добро пожаловать в Персональный помощник!
        Выберите действие:
        1. Управление заметками
        2. Управление задачами
        3. Управление контактами
        4. Управление финансовыми записями
        5. Калькулятор
        6. Выход
        """)

    def run(self):
        while True:
            self.display_menu()
            choice = input('Введите номер действия: ').strip()
            action = self.menu_options.get(choice)
            if action:
                try:
                    action()
                except Exception as er:
                    print(f'Произошла ошибка: {er}')
            else:
                print('Некорректный выбор. Попробуйте снова')

    def manage_notes(self):
        while True:
            print('\nУправление заметками:')
            print('1. Создать заметку')
            print('2. Список заметок')
            print('3. Детали заметки')
            print('4. Редактировать заметку')
            print('5. Удалить заметку')
            print('6. Экспорт в CSV')
            print('7. Импорт из CSV')
            print('8. Назад')
            choice = input('Выберите действие: ').strip()
            if choice == '1':
                title = input('Введите заголовок: ').strip()
                content = input('Введите содержимое: ').strip()
                self.note_manager.create_note(title, content)
            elif choice == '2':
                self.note_manager.list_notes()
            elif choice == '3':
                try:
                    note_id = int(input('Введите ID заметки: '))
                    self.note_manager.view_note_details(note_id)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '4':
                try:
                    note_id = int(input('Введите ID заметки: '))
                    new_title = input('Введите новый заголовок: ').strip()
                    new_content = input('Введите новое содержимое: ').strip()
                    self.note_manager.edit_note(note_id, new_title, new_content)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '5':
                try:
                    note_id = int(input('Введите ID заметки: '))
                    self.note_manager.delete_note(note_id)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '6':
                file_name = input('Введите имя файла для экспорта (например, notes.csv): ').strip()
                self.note_manager.export_to_csv(file_name)
            elif choice == '7':
                file_name = input('Введите имя файла для импорта (например, notes.csv): ').strip()
                self.note_manager.import_from_csv(file_name)
            elif choice == '8':
                break
            else:
                print('Некорректный выбор')

    def manage_tasks(self):
        while True:
            print('\nУправление задачами:')
            print('1. Добавить задачу')
            print('2. Список задач')
            print('3. Отметить задачу как выполненную')
            print('4. Редактировать задачу')
            print('5. Удалить задачу')
            print('6. Экспорт в CSV')
            print('7. Импорт из CSV')
            print('8. Назад')
            choice = input('Выберите действие: ').strip()
            if choice == '1':
                title = input('Введите заголовок: ').strip()
                description = input('Введите описание: ').strip()
                priority = input('Введите приоритет (Высокий/Средний/Низкий): ').strip()
                due_date = input('Введите срок выполнения (ДД.ММ.ГГГГ): ').strip()
                self.task_manager.add_task(title, description, priority, due_date)
            elif choice == '2':
                self.task_manager.list_tasks()
            elif choice == '3':
                try:
                    task_id = int(input('Введите ID задачи: ').strip())
                    self.task_manager.mark_task_done(task_id)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '4':
                try:
                    task_id = int(input('Введите ID задачи: ').strip())
                    new_title = input('Введите новый заголовок: ').strip()
                    new_description = input('Введите новое описание: ').strip()
                    new_priority = input('Введите новый приоритет (высокий/средний/низкий): ').strip()
                    new_due_date = input('Введите новый срок выполнения (ДД.ММ.ГГГГ): ').strip()
                    self.task_manager.edit_task(task_id, new_title, new_description, new_priority, new_due_date)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '5':
                try:
                    task_id = int(input('Введите ID задачи: ').strip())
                    self.task_manager.delete_task(task_id)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '6':
                file_name = input('Введите имя файла для экспорта (например, tasks.csv): ').strip()
                self.task_manager.export_to_csv(file_name)
            elif choice == '7':
                file_name = input('Введите имя файла для импорта (например, tasks.csv): ').strip()
                self.task_manager.import_from_csv(file_name)
            elif choice == '8':
                break
            else:
                print('Некорректный выбор')

    def manage_contacts(self):
        while True:
            print('\nУправление контактами:')
            print('1. Добавить контакт')
            print('2. Найти контакт')
            print('3. Редактировать контакт')
            print('4. Удалить контакт')
            print('5. Экспорт в CSV')
            print('6. Импорт из CSV')
            print('7. Назад')
            choice = input('Выберите действие: ').strip()
            if choice == '1':
                name = input('Введите имя: ').strip()
                phone = input('Введите номер телефона: ').strip()
                email = input('Введите email: ').strip()
                self.contact_manager.add_contact(name, phone, email)
            elif choice == '2':
                search_term = input('Введите имя или номер телефона для поиска: ').strip()
                self.contact_manager.search_contact(search_term)
            elif choice == '3':
                try:
                    contact_id = int(input('Введите ID контакта: ').strip())
                    new_name = input('Введите новое имя: ').strip()
                    new_phone = input('Введите новый номер телефона: ').strip()
                    new_email = input('Введите новый email: ').strip()
                    self.contact_manager.edit_contact(contact_id, new_name, new_phone, new_email)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '4':
                try:
                    contact_id = int(input('Введите ID контакта: ').strip())
                    self.contact_manager.delete_contact(contact_id)
                except ValueError:
                    print('ID должен быть числом')
            elif choice == '5':
                file_name = input('Введите имя файла для экспорта (например, contacts.csv): ').strip()
                self.contact_manager.export_to_csv(file_name)
            elif choice == '6':
                file_name = input('Введите имя файла для импорта (например, contacts.csv): ').strip()
                self.contact_manager.import_from_csv(file_name)
            elif choice == '7':
                break
            else:
                print('Некорректный выбор')
    def manage_financial_records(self):
        while True:
            print('\nУправление финансовыми записями:')
            print('1. Добавить запись')
            print('2. Список записей')
            print('3. Генерация отчёта')
            print('4. Экспорт в CSV')
            print('5. Импорт из CSV')
            print('6. Назад')
            choice = input('Выберите действие: ').strip()
            if choice == '1':
                try:
                    amount = float(input('Введите сумму (положительное для дохода, отрицательное для расхода): ').strip())
                    category = input('Введите категорию: ').strip()
                    date = input('Введите дату операции (ДД.ММ.ГГГГ): ').strip()
                    description = input('Введите описание: ').strip()
                    self.finance_manager.add_record(amount, category, date, description)
                except ValueError:
                    print('Некорректный ввод суммы')
            elif choice == '2':
                category = input('Введите категорию для фильтрации (или оставьте пустым): ').strip()
                date_range = input('Введите диапазон дат (например, 01.01.2023-31.01.2023) или оставьте пустым: ').strip()
                if date_range:
                    start_date, end_date = date_range.split('-')
                    self.finance_manager.list_records(category, [start_date.strip(), end_date.strip()])
                else:
                    self.finance_manager.list_records(category)
            elif choice == '3':
                try:
                    start_date = input('Введите начальную дату (ДД.ММ.ГГГГ): ').strip()
                    end_date = input('Введите конечную дату (ДД.ММ.ГГГГ): ').strip()
                    self.finance_manager.generate_report(start_date, end_date)
                except ValueError:
                    print('Некорректный ввод дат')
            elif choice == '4':
                file_name = input('Введите имя файла для экспорта (например, finance.csv): ').strip()
                self.finance_manager.export_to_csv(file_name)
            elif choice == '5':
                file_name = input('Введите имя файла для импорта (например, finance.csv): ').strip()
                self.finance_manager.import_from_csv(file_name)
            elif choice == '6':
                break
            else:
                print('Некорректный выбор')

    def manage_calculator(self):
        while True:
            print('\nКалькулятор:')
            print('Введите математическое выражение для вычисления или "назад" для выхода')
            expression = input('Выражение: ').strip()
            if expression.lower() == 'назад':
                break
            result = self.calculator.calculate(expression)
            print(f'Результат: {result}')

    def exit_program(self):
        print('Хорошего дня!')
        sys.exit(0)


if __name__ == "__main__":
    app = PersonalAssistant()
    app.run()
