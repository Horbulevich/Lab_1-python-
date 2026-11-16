import os
import FreeSimpleGUI as sg

import functions
import core


def format_todos(todos):
    result = []

    for number, todo in enumerate(todos, start=1):
        status = "✓" if todo.get("completed", False) else " "
        deadline = todo.get("deadline", "") or "без терміну"
        result.append(
            f"{number}. [{status}] {todo.get('text', '')} | до: {deadline}"
        )

    return result


def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(functions.FILEPATH):
        functions.write_todos([])

    todos = functions.get_todos()

    layout = [
        [sg.Text("Текст завдання"), sg.Input(key="text", size=(35, 1))],
        [sg.Text("Термін (РРРР-ММ-ДД)"), sg.Input(key="deadline", size=(18, 1))],
        [
            sg.Button("Додати", key="add"),
            sg.Button("Редагувати", key="edit"),
            sg.Button("Виконано", key="done"),
            sg.Button("Видалити", key="delete")
        ],
        [sg.Listbox(values=format_todos(todos), key="todos", size=(65, 12), enable_events=True)],
        [
            sg.Button("Кількість", key="count"),
            sg.Button("Резервна копія", key="backup"),
            sg.Button("Очистити", key="clear"),
            sg.Button("Вихід", key="exit")
        ]
    ]

    window = sg.Window("TaskHub", layout, font=("Arial", 12))

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "exit"):
            break

        try:
            if event == "add":
                core.add_todo(
                    todos,
                    values["text"].strip(),
                    values["deadline"].strip()
                )
                window["text"].update("")
                window["deadline"].update("")

            elif event == "todos":
                indexes = window["todos"].get_indexes()
                if indexes:
                    todo = todos[indexes[0]]
                    window["text"].update(todo.get("text", ""))
                    window["deadline"].update(todo.get("deadline", ""))

            elif event == "edit":
                indexes = window["todos"].get_indexes()
                if not indexes:
                    sg.popup_error("Оберіть завдання.")
                    continue

                deadline = values["deadline"].strip()
                core.edit_todo(
                    todos,
                    indexes[0] + 1,
                    values["text"].strip(),
                    deadline if deadline else None
                )

            elif event == "done":
                indexes = window["todos"].get_indexes()
                if not indexes:
                    sg.popup_error("Оберіть завдання.")
                    continue
                core.complete_todo(todos, indexes[0] + 1)

            elif event == "delete":
                indexes = window["todos"].get_indexes()
                if not indexes:
                    sg.popup_error("Оберіть завдання.")
                    continue
                core.delete_todo(todos, indexes[0] + 1)
                window["text"].update("")
                window["deadline"].update("")

            elif event == "count":
                sg.popup(f"Кількість завдань: {core.count_todos(todos)}")

            elif event == "backup":
                backup_file = core.backup_todos()
                sg.popup(f"Резервну копію створено:\n{backup_file}")

            elif event == "clear":
                answer = sg.popup_yes_no("Очистити весь список завдань?")
                if answer == "Yes":
                    core.clear_todos(todos)
                    window["text"].update("")
                    window["deadline"].update("")

            window["todos"].update(values=format_todos(todos))

        except (ValueError, IndexError, OSError) as error:
            sg.popup_error(str(error))

    window.close()


if __name__ == "__main__":
    main()
