import json
import csv
from datetime import datetime
from typing import List, Optional
from func import read_csv, write_csv

class FinanceRecord:
    def __init__(self, record_id: int, amount: float, category: str, date: str, description: str):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['amount'], data['category'], data['date'], data['description'])


class FinanceManager:
    def __init__(self, storage_file: str = 'finance.json'):
        self.storage_file = storage_file
        self.records: List[FinanceRecord] = self.load_records()

    def load_records(self) -> List[FinanceRecord]:
        try:
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                return [FinanceRecord.from_dict(record) for record in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_records(self):
        with open(self.storage_file, 'w') as file:
            json.dump([record.to_dict() for record in self.records], file, indent=4)

    def add_record(self, amount: float, category: str, date: str, description: str):
        record_id = max([record.id for record in self.records], default=0) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()
        print(f'Запись на сумму {amount} в категории "{category}" успешно добавлена')

    def list_records(self, category: Optional[str] = None, date_range: Optional[List[str]] = None):
        filtered_records = self.records
        if category:
            filtered_records = [record for record in filtered_records if record.category.lower() == category.lower()]
        if date_range:
            start_date, end_date = [datetime.strptime(date, '%d.%m.%Y') for date in date_range]
            filtered_records = [
                record for record in filtered_records
                if start_date <= datetime.strptime(record.date, '%d.%m.%Y') <= end_date
            ]
        if not filtered_records:
            print('Записей не найдено')
        else:
            for record in filtered_records:
                print(f'ID: {record.id}, Amount: {record.amount}, Category: {record.category}, '
                      f'Date: {record.date}, Description: {record.description}')

    def generate_report(self, start_date: str, end_date: str):
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
        filtered_records = [
            record for record in self.records
            if start_date <= datetime.strptime(record.date, '%d.%m.%Y') <= end_date
        ]
        income = sum(record.amount for record in filtered_records if record.amount > 0)
        expenses = sum(record.amount for record in filtered_records if record.amount < 0)
        balance = income + expenses
        print(f'Отчёт за период с {start_date.strftime("%d.%m.%Y")} по {end_date.strftime("%d.%m.%Y")}:')
        print(f'- Общий доход: {income}')
        print(f'- Общие расходы: {abs(expenses)}')
        print(f'- Баланс: {balance}')

    def export_to_csv(self, file_name):
        write_csv(file_name, [record.to_dict() for record in self.records], ['id', 'amount', 'category', 'date', 'description'])
        print(f'Финансовые записи успешно экспортированы в {file_name}')

    def import_from_csv(self, file_name):
        data = read_csv(file_name)
        for row in data:
            self.add_record(float(row['amount']), row['category'], row['date'], row['description'])
        print(f'Финансовые записи успешно импортированы из {file_name}')
