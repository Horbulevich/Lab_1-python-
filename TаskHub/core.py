import shutil
from datetime import datetime
from pathlib import Path

import functions


DATE_FORMAT = "%Y-%m-%d"


def check_date(date):
    if not date:
        return True

    try:
        datetime.strptime(date, DATE_FORMAT)
        return True
    except ValueError:
        return False


def check_number(todos, number):
    if number < 1 or number > len(todos):
        raise IndexError


def add_todo(todos, text, deadline=""):
    """Додає завдання, перевіряє дублікати та зберігає список."""
    text = text.strip()

    if not text:
        raise ValueError("Текст завдання не може бути порожнім.")

    if any(todo.get("text", "").lower() == text.lower() for todo in todos):
        raise ValueError("Таке завдання вже існує.")

    if not check_date(deadline):
        raise ValueError("Неправильна дата. Використовуйте формат РРРР-ММ-ДД.")

    todo = {
        "text": text,
        "completed": False,
        "deadline": deadline
    }

    todos.append(todo)
    functions.write_todos(todos)
    return todo


def edit_todo(todos, number, new_text, deadline=None):
    """Змінює текст завдання та за потреби його термін."""
    check_number(todos, number)
    new_text = new_text.strip()

    if not new_text:
        raise ValueError("Текст завдання не може бути порожнім.")

    for index, todo in enumerate(todos):
        if index != number - 1 and todo.get("text", "").lower() == new_text.lower():
            raise ValueError("Таке завдання вже існує.")

    if deadline is not None and not check_date(deadline):
        raise ValueError("Неправильна дата. Використовуйте формат РРРР-ММ-ДД.")

    todos[number - 1]["text"] = new_text

    if deadline is not None:
        todos[number - 1]["deadline"] = deadline

    functions.write_todos(todos)
    return todos[number - 1]


def complete_todo(todos, number):
    """Перемикає статус завдання: виконане / невиконане."""
    check_number(todos, number)
    todos[number - 1]["completed"] = not todos[number - 1].get("completed", False)
    functions.write_todos(todos)
    return todos[number - 1]


def delete_todo(todos, number):
    """Видаляє завдання за номером."""
    check_number(todos, number)
    deleted = todos.pop(number - 1)
    functions.write_todos(todos)
    return deleted


def count_todos(todos):
    return len(todos)


def clear_todos(todos):
    todos.clear()
    functions.write_todos(todos)


def search_todos(todos, text):
    text = text.lower().strip()
    return [todo for todo in todos if text in todo.get("text", "").lower()]


def backup_todos(filepath=functions.FILEPATH):
    """Створює копію JSON-файлу та повертає шлях до неї."""
    source = Path(filepath)

    if not source.exists():
        raise FileNotFoundError("Файл із завданнями ще не створений.")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = source.with_name(
        f"{source.stem}-backup-{timestamp}{source.suffix}"
    )

    shutil.copy2(source, backup)
    return backup
