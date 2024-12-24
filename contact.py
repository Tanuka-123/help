import json
import csv
from typing import List, Optional
from func import read_csv, write_csv

class Contact:
    def __init__(self, contact_id: int, name: str, phone: str, email: str):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['name'], data['phone'], data['email'])


class ContactManager:
    def __init__(self, storage_file: str = 'contacts.json'):
        self.storage_file = storage_file
        self.contacts: List[Contact] = self.load_contacts()

    def load_contacts(self) -> List[Contact]:
        try:
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                return [Contact.from_dict(contact) for contact in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        with open(self.storage_file, 'w') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def add_contact(self, name: str, phone: str, email: str):
        contact_id = max([contact.id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print(f'Контакт "{name}" успешно добавлен.')

    def search_contact(self, search_term: str):
        results = [
            contact for contact in self.contacts
            if search_term.lower() in contact.name.lower() or search_term in contact.phone
        ]
        if results:
            for contact in results:
                print(f'ID: {contact.id}, Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}')
        else:
            print('Контакт не найден')

    def edit_contact(self, contact_id: int, new_name: str, new_phone: str, new_email: str):
        contact = next((contact for contact in self.contacts if contact.id == contact_id), None)
        if contact:
            contact.name = new_name
            contact.phone = new_phone
            contact.email = new_email
            self.save_contacts()
            print(f'Контакт с ID {contact_id} успешно обновлен')
        else:
            print('Контакт не найден')

    def delete_contact(self, contact_id: int):
        self.contacts = [contact for contact in self.contacts if contact.id != contact_id]
        self.save_contacts()
        print(f'Контакт с ID {contact_id} успешно удален')

    def export_to_csv(self, file_name: str):
        write_csv(file_name, [contact.to_dict() for contact in self.contacts], ['id', 'name', 'phone', 'email'])
        print(f'Контакты успешно экспортированы в {file_name}')

    def import_from_csv(self, file_name: str):
        data = read_csv(file_name)
        for row in data:
            self.add_contact(row['name'], row['phone'], row['email'])
        print(f'Контакты успешно импортированы из {file_name}')
