import json
import csv
from datetime import datetime
from typing import List, Optional
from func import read_csv, write_csv

class Note:
    def __init__(self, note_id: int, title: str, content: str, timestamp: Optional[str] = None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['title'], data['content'], data['timestamp'])


class NoteManager:
    def __init__(self, storage_file: str = 'notes.json'):
        self.storage_file = storage_file
        self.notes: List[Note] = self.load_notes()

    def load_notes(self) -> List[Note]:
        try:
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                return [Note.from_dict(note) for note in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open(self.storage_file, 'w') as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=4)

    def create_note(self, title: str, content: str):
        note_id = max([note.id for note in self.notes], default=0) + 1
        new_note = Note(note_id, title, content)
        self.notes.append(new_note)
        self.save_notes()
        print(f'Заметка "{title}" успешно создана')

    def list_notes(self):
        if not self.notes:
            print('Нет доступных заметок')
        else:
            for note in self.notes:
                print(f'ID: {note.id}, Title: {note.title}, Timestamp: {note.timestamp}')

    def view_note_details(self, note_id: int):
        note = next((note for note in self.notes if note.id == note_id), None)
        if note:
            print(f'ID: {note.id}')
            print(f'Title: {note.title}')
            print(f'Content: {note.content}')
            print(f'Timestamp: {note.timestamp}')
        else:
            print('Заметка не найдена')

    def edit_note(self, note_id: int, new_title: str, new_content: str):
        note = next((note for note in self.notes if note.id == note_id), None)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            self.save_notes()
            print(f'Заметка "{new_title}" успешно обновлена')
        else:
            print('Заметка не найдена')

    def delete_note(self, note_id: int):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()
        print(f'Заметка с ID {note_id} успешно удалена')

    def export_to_csv(self, file_name):
        write_csv(file_name, [note.to_dict() for note in self.notes], ['id', 'title', 'content', 'timestamp'])
        print(f'Заметки успешно экспортированы в {file_name}')


    def import_from_csv(self, file_name):
        data = read_csv(file_name)
        for row in data:
            self.create_note(row['title'], row['content'])
        print(f'Заметки успешно импортированы из {file_name}')