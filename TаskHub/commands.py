import core


def get_number(argument):
    try:
        return int(argument)
    except ValueError:
        raise ValueError("Введіть цілий номер завдання.")


def do_add(todos, argument):
    if not argument.strip():
        print("\tВведіть текст завдання.")
        return True

    deadline = input("Термін виконання (РРРР-ММ-ДД) або Enter: ").strip()
    core.add_todo(todos, argument, deadline)
    print("\tЗавдання додано.")
    return True


def do_show(todos, argument):
    if not todos:
        print("\tСписок порожній.")
        return True

    for number, todo in enumerate(todos, start=1):
        status = "✓" if todo.get("completed", False) else " "
        deadline = todo.get("deadline", "") or "без терміну"
        print(f"{number}. [{status}] {todo.get('text', '')} | до: {deadline}")

    return True


def do_edit(todos, argument):
    number = get_number(argument)
    new_text = input("Введіть новий текст: ").strip()
    core.edit_todo(todos, number, new_text)
    print("\tЗавдання змінено.")
    return True


def do_complete(todos, argument):
    number = get_number(argument)
    todo = core.complete_todo(todos, number)

    if todo["completed"]:
        print(f"\tВиконано: {todo['text']}")
    else:
        print(f"\tЗавдання знову активне: {todo['text']}")

    return True


def do_delete(todos, argument):
    number = get_number(argument)
    deleted = core.delete_todo(todos, number)
    print(f"\tВидалено: {deleted['text']}")
    return True


def do_count(todos, argument):
    print(f"Кількість завдань: {core.count_todos(todos)}")
    return True


def do_clear(todos, argument):
    answer = input("Очистити весь список? (так/ні): ").strip().lower()

    if answer == "так":
        core.clear_todos(todos)
        print("Список завдань очищено.")
    else:
        print("Очищення скасовано.")

    return True


def do_backup(todos, argument):
    backup_file = core.backup_todos()
    print(f"Резервну копію створено: {backup_file}")
    return True


def do_search(todos, argument):
    if not argument.strip():
        print("Введіть слово для пошуку.")
        return True

    found = core.search_todos(todos, argument)

    if not found:
        print("Завдань не знайдено.")
    else:
        for todo in found:
            status = "виконано" if todo.get("completed", False) else "активне"
            print(f"- {todo.get('text', '')} ({status})")

    return True


def do_help(todos, argument):
    print("\nДоступні команди:")
    print("add текст    - додати завдання")
    print("show         - показати список")
    print("edit номер   - редагувати завдання")
    print("done номер   - змінити статус виконання")
    print("delete номер - видалити завдання")
    print("search слово - знайти завдання")
    print("count        - порахувати завдання")
    print("clear        - очистити список")
    print("backup       - створити резервну копію")
    print("help         - показати команди")
    print("exit         - завершити програму")
    return True


def do_exit(todos, argument):
    print("Роботу програми завершено.")
    return False


COMMANDS = {
    "add": do_add,
    "show": do_show,
    "edit": do_edit,
    "done": do_complete,
    "complete": do_complete,
    "delete": do_delete,
    "count": do_count,
    "clear": do_clear,
    "backup": do_backup,
    "search": do_search,
    "help": do_help,
    "exit": do_exit
}


def dispatch(todos, user_action):
    parts = user_action.strip().split(maxsplit=1)

    if not parts:
        print("Введіть команду.")
        return True

    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else ""
    handler = COMMANDS.get(command)

    if handler is None:
        print("Невідома команда. Введіть help.")
        return True

    try:
        return handler(todos, argument)
    except ValueError as error:
        print(error)
        return True
    except IndexError:
        print("Невірний номер завдання.")
        return True
    except OSError as error:
        print(f"Помилка роботи з файлом: {error}")
        return True
