import argparse
import os
import sys
from typing import List

import functions
import commands

try:
    import click
except ImportError:
    click = None

try:
    import typer
except ImportError:
    typer = None


def repl():
    """Інтерактивний режим роботи з командами."""
    todos = functions.get_todos()
    print("=== TASKHUB CLI ===")
    print("Введіть help, щоб переглянути доступні команди.")

    while True:
        user_action = input("\nTaskHub > ")
        if not commands.dispatch(todos, user_action):
            break


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python cli.py",
        description="TaskHub — консольний список завдань."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("show", help="Показати список")

    add = sub.add_parser("add", help="Додати завдання")
    add.add_argument("text", nargs="+", help="Текст завдання")

    edit = sub.add_parser("edit", help="Редагувати завдання")
    edit.add_argument("number", type=int, help="Номер завдання")

    done = sub.add_parser("done", help="Змінити статус завдання")
    done.add_argument("number", type=int, help="Номер завдання")

    delete = sub.add_parser("delete", help="Видалити завдання")
    delete.add_argument("number", type=int, help="Номер завдання")

    search = sub.add_parser("search", help="Знайти завдання")
    search.add_argument("text", nargs="+", help="Слово для пошуку")

    sub.add_parser("count", help="Порахувати завдання")
    sub.add_parser("clear", help="Очистити список")
    sub.add_parser("backup", help="Створити резервну копію")
    sub.add_parser("repl", help="Запустити діалоговий режим")

    return parser


def run_from_args(args):
    if args.command == "repl":
        repl()
        return

    todos = functions.get_todos()

    if args.command == "add":
        commands.dispatch(todos, "add " + " ".join(args.text))
    elif args.command == "show":
        commands.dispatch(todos, "show")
    elif args.command == "edit":
        commands.dispatch(todos, f"edit {args.number}")
    elif args.command == "done":
        commands.dispatch(todos, f"done {args.number}")
    elif args.command == "delete":
        commands.dispatch(todos, f"delete {args.number}")
    elif args.command == "search":
        commands.dispatch(todos, "search " + " ".join(args.text))
    elif args.command in ("count", "clear", "backup"):
        commands.dispatch(todos, args.command)


def run_command(action):
    commands.dispatch(functions.get_todos(), action)


# Click — 1 альтернативний спосіб запуску тих самих команд.
click_cli = None
if click is not None:
    @click.group(help="TaskHub через Click")
    def click_cli():
        pass

    @click_cli.command("show")
    def click_show():
        run_command("show")

    @click_cli.command("add")
    @click.argument("text", nargs=-1, required=True)
    def click_add(text):
        run_command("add " + " ".join(text))

    @click_cli.command("edit")
    @click.argument("number", type=int)
    def click_edit(number):
        run_command(f"edit {number}")

    @click_cli.command("done")
    @click.argument("number", type=int)
    def click_done(number):
        run_command(f"done {number}")

    @click_cli.command("delete")
    @click.argument("number", type=int)
    def click_delete(number):
        run_command(f"delete {number}")

    @click_cli.command("search")
    @click.argument("text", nargs=-1, required=True)
    def click_search(text):
        run_command("search " + " ".join(text))

    @click_cli.command("count")
    def click_count():
        run_command("count")

    @click_cli.command("clear")
    def click_clear():
        run_command("clear")

    @click_cli.command("backup")
    def click_backup():
        run_command("backup")

    @click_cli.command("repl")
    def click_repl():
        repl()


# Typer — 2 альтернативний спосіб запуску тих самих команд.
typer_app = None
if typer is not None:
    typer_app = typer.Typer(help="TaskHub через Typer")

    @typer_app.command("show")
    def typer_show():
        run_command("show")

    @typer_app.command("add")
    def typer_add(text: List[str] = typer.Argument(...)):
        run_command("add " + " ".join(text))

    @typer_app.command("edit")
    def typer_edit(number: int = typer.Argument(...)):
        run_command(f"edit {number}")

    @typer_app.command("done")
    def typer_done(number: int = typer.Argument(...)):
        run_command(f"done {number}")

    @typer_app.command("delete")
    def typer_delete(number: int = typer.Argument(...)):
        run_command(f"delete {number}")

    @typer_app.command("search")
    def typer_search(text: List[str] = typer.Argument(...)):
        run_command("search " + " ".join(text))

    @typer_app.command("count")
    def typer_count():
        run_command("count")

    @typer_app.command("clear")
    def typer_clear():
        run_command("clear")

    @typer_app.command("backup")
    def typer_backup():
        run_command("backup")

    @typer_app.command("repl")
    def typer_repl():
        repl()


def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(functions.FILEPATH):
        functions.write_todos([])

    if len(sys.argv) == 1:
        repl()
        return

    if sys.argv[1] == "click":
        if click_cli is None:
            print("Для Click встановіть бібліотеку: python -m pip install click")
        else:
            click_cli(args=sys.argv[2:], prog_name="python cli.py click")
        return

    if sys.argv[1] == "typer":
        if typer_app is None:
            print("Для Typer встановіть бібліотеку: python -m pip install typer")
        else:
            typer_app(args=sys.argv[2:], prog_name="python cli.py typer")
        return

    parser = build_parser()
    args = parser.parse_args()
    run_from_args(args)


if __name__ == "__main__":
    main()
