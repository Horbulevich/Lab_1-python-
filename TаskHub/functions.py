import json
import os

FILEPATH = os.path.join("data", "todos.json")


def get_todos(filepath=FILEPATH):
    """Зчитує завдання з JSON-файлу."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            todos = json.load(file)
            return todos if isinstance(todos, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_todos(todos, filepath=FILEPATH):
    """Зберігає завдання у JSON-файлі."""
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(todos, file, ensure_ascii=False, indent=4)
