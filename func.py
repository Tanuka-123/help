import csv


def read_csv(file_name):
    try:
        with open(file_name, 'r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f'Файл {file_name} не найден')
        return []
    except Exception as er:
        print(f'Ошибка при чтении файла {file_name}: {er}')
        return []


def write_csv(file_name, data, fieldnames):
    try:
        with open(file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as er:
        print(f'Ошибка при записи файла {file_name}: {er}')